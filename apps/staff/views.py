from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import openpyxl
from django.http import HttpResponse
from apps.institute.models import InstituteMaster
from .models import StaffMaster, StaffAttendance, StaffLeave
from .forms import StaffMasterForm, StaffAttendanceForm, StaffLeaveForm
from apps.course.models import CourseMaster
from apps.accounts.models import CustomUser
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import IntegrityError
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.utils import timezone


def staff_report(request):
    return render(request, 'staff/report.html')

def staff_attendance_report(request):
    search_query = request.GET.get('q', '')
    staff_id = request.GET.get('staff_id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Start with all attendance records
    attendance_list = StaffAttendance.objects.all()

    # Apply search filters
    if search_query:
        attendance_list = attendance_list.filter(
            Q(staff_id__name__icontains=search_query) |   # Search staff name
            Q(status__iexact=search_query) |              # Use iexact for status
            Q(date__icontains=search_query) |             # Search by date
            Q(staff_id__id__icontains=search_query) |     # Search by staff ID
            Q(submitted_by__username__icontains=search_query)  # Search by submitted_by username
        )

    if staff_id:
        attendance_list = attendance_list.filter(staff_id__id__icontains=staff_id)
    if start_date:
        attendance_list = attendance_list.filter(date__gte=start_date)
    if end_date:
        attendance_list = attendance_list.filter(date__lte=end_date)

    # Handle Excel export for filtered data
    if 'export' in request.GET:  # If "Export" button is clicked
        return export_attendance_to_excel(attendance_list)  # Export only filtered data
    
    # Add pagination
    paginator = Paginator(attendance_list, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    attendance_list = paginator.get_page(page_number)

    return render(request, 'staff/staff_attendance_report.html', {
        'attendance_list': attendance_list,
        'search_query': search_query,
        
    })

def export_attendance_to_excel(attendance_list):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Staff Attendance Report'

    # Define the column titles
    columns = ['Sr No', 'Staff ID', 'Name', 'Date', 'Status', 'Submitted By']
    worksheet.append(columns)

    # Iterate over the filtered attendance_list and write to the worksheet
    for idx, attendance in enumerate(attendance_list, 1):
        worksheet.append([
            idx,
            attendance.staff_id.id,
            attendance.staff_id.name,
            attendance.date,
            attendance.status,
            attendance.submitted_by.username if attendance.submitted_by else 'N/A',
        ])
    
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=staff_attendance_report.xlsx'
    
    # Save the workbook to the response
    workbook.save(response)

    return response


def staff_leave_report(request):
    search_query = request.GET.get('q', '')
    staff_id_filter = request.GET.get('staff_id', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    leave_records = StaffLeave.objects.all()
    if search_query:
        leave_records = leave_records.filter(
            Q(staff_id__name__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(start__icontains=search_query) |
            Q(end__icontains=search_query) |
            Q(staff_id__id__icontains=search_query) |
            Q(approved_by__username__icontains=search_query)
        )
    if staff_id_filter:
        leave_records = leave_records.filter(staff_id__id__icontains=staff_id_filter)
    if start_date_filter:
        leave_records = leave_records.filter(start__gte=start_date_filter)
    if end_date_filter:
        leave_records = leave_records.filter(end__lte=end_date_filter)

    if 'export' in request.GET:  # If "Export" button is clicked
        return export_leave_to_excel(leave_records) 
    
    paginator = Paginator(leave_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'leave_list': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'staff_id_filter': staff_id_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    }
    return render(request, 'staff/staff_leave_report.html', context)

def export_leave_to_excel(leave_records):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Staff Leave Report'

    # Define the column titles
    columns = ['Sr No', 'Staff ID', 'Name', 'Start Date', 'End Date', 'Status', 'Approved By']
    worksheet.append(columns)

    # Iterate over leave_records and write to the worksheet
    for idx, leave in enumerate(leave_records, 1):
        worksheet.append([
            idx,
            leave.staff_id.id,
            leave.staff_id.name,
            leave.start,
            leave.end,
            leave.status,
            leave.approved_by.username if leave.approved_by else 'N/A',
        ])

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=staff_leave_report.xlsx'

    # Save the workbook to the response
    workbook.save(response)
    return response

def staff_list(request):
    institute_user = request.user.inst_id
    search_query = request.GET.get('q', '')  # Get the search query from the GET parameters
    staff_id_filter = request.GET.get('staff_id', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    # Filter staff by search query
    staff_queryset = StaffMaster.objects.filter(institute=institute_user).filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(pincode__icontains=search_query) |
        Q(number__icontains=search_query) |
        Q(status__icontains=search_query) |      
        Q(role__icontains=search_query)
    )
    
    if staff_id_filter:
        staff_queryset = staff_queryset.filter(id__icontains=staff_id_filter)
    if start_date_filter:
        staff_queryset = staff_queryset.filter(start__gte=start_date_filter)
    if end_date_filter:
        staff_queryset = staff_queryset.filter(end__lte=end_date_filter)
    
    paginator = Paginator(staff_queryset, 10)  # Show 10 staff per page
    page_number = request.GET.get('page')
    staffs = paginator.get_page(page_number)
    
    context = {
        'staff_list': staffs,  # This will now contain the paginated and filtered queryset
        'search_query': search_query,  # Pass the search query back to the template
        'user_role': request.user.role,
    }
    return render(request, 'staff/staff-view.html', context)

def toggle_staff_status(request, pk):
    staff = get_object_or_404(StaffMaster, pk=pk)

    if staff.status == 'active':
        staff.status = 'inactive'
        staff.do_leaving = timezone.now()  # Set the current date and time to do_leaving
        messages.success(request, f"{staff.name} has been deactivated.")

        # Send deactivation email
        send_mail(
            subject='Your Account has been Deactivated',
            message=f'Dear {staff.name},\n\nYour account has been deactivated on {staff.do_leaving.date()}.\nIf you have any questions, please contact the administration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[staff.email],  # Ensure staff.email is a valid email field
        )
    else:
        staff.status = 'active'
        staff.do_leaving = None  # Clear the do_leaving date if activating back
        messages.success(request, f"{staff.name} has been activated.")

        # Send activation email
        send_mail(
            subject='Your Account has been Activated',
            message=f'Dear {staff.name},\n\nYour account has been activated again. You can now access your profile.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[staff.email],
        )

    staff.save()
    return redirect('staff_list')

def staff_detail(request, pk):
    staff = get_object_or_404(StaffMaster, pk=pk)
    return render(request, 'staff/staff_detail.html', {'staff': staff})

def staff_create(request):
    courses = CourseMaster.objects.all()
    institute_user = request.user.inst_id  # Retrieve the institute ID from the logged-in user
    if request.method == 'POST':
        form = StaffMasterForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.institute = institute_user  # Assign the institute to the staff
         
               

            if staff.role == "teacher" and not staff.course:
                messages.error(request, 'Course is required when the role is Teacher.')
                return render(request, 'staff/staff.html', {'form': form, 'courses': courses})
            
            
            default_password = get_random_string(length=6)
            hashed_password = make_password(default_password)
            
            if CustomUser.objects.filter(email=staff.email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'staff/staff.html', {'form': form})
            
            staff.save()
            
            # Create CustomUser instance
            user = CustomUser(
                email=staff.email,
                username=staff.email,
                mobile=staff.number,
                password=hashed_password,
                is_staff=True,
                role=staff.role,
                first_name=staff.name,
                address=f"{staff.address}, {staff.state}, {staff.district}",
                inst_id=institute_user  # Set the institute ID here
            )
            user.save()

            # Handle profile image
            profile_image = staff.profile
            if profile_image:
                image_name = profile_image.name
                image_content = profile_image.read()
                profile_image_file = ContentFile(image_content, image_name)
                user.profile_image.save(image_name, profile_image_file)
                staff.user = user
                staff.save()

            # Send registration email
            send_mail(
                'Registration Successful',
                f'Hi,\n\nYour registration was successful. Your password is: {default_password}\n\nPlease log in at: http://127.0.0.1:8000/accounts/login/',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Staff member created successfully.')
            return redirect('staff_create')
        else:
            messages.error(request, 'Form data is invalid.')
    else:
        form = StaffMasterForm()

    context = {'form': form, 'courses': courses}
    return render(request, 'staff/staff.html', context)


def staff_update(request, pk):
    staff = get_object_or_404(StaffMaster, pk=pk)
    if request.method == 'POST':
        print('hello')

        form = StaffMasterForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'data updated successfully!')
            return redirect('staff_detail',pk=staff.pk)
    else:
        form = StaffMasterForm(instance=staff)
    return render(request, 'staff/staff-edit.html', {'form': form})

def staff_attendance_list(request):
    search_query = request.GET.get('q', '')
    staff_id_filter = request.GET.get('staff_id', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    attendance_records = StaffAttendance.objects.all()
    if search_query:
        attendance_records = attendance_records.filter(
            Q(staff_id__name__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(date__icontains=search_query) |
            Q(staff_id__id__icontains=search_query) |
            Q(submitted_by__username__icontains=search_query)
        )
    if staff_id_filter:
        attendance_records = attendance_records.filter(staff_id__id__icontains=staff_id_filter)
    if start_date_filter:
        attendance_records = attendance_records.filter(start__gte=start_date_filter)
    if end_date_filter:
        attendance_records = attendance_records.filter(end__lte=end_date_filter)
    
    paginator = Paginator(attendance_records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff/attendance-view.html', {
        'attendance_list': page_obj, 
        'search_query': search_query
    })

def staff_leave_list(request):
    search_query = request.GET.get('q', '')
    staff_id_filter = request.GET.get('staff_id', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    leave_records = StaffLeave.objects.all()
    if search_query:
        leave_records = leave_records.filter(
            Q(staff_id__name__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(start__icontains=search_query) |
            Q(end__icontains=search_query) |
            Q(staff_id__id__icontains=search_query) |
            Q(approved_by__username__icontains=search_query)
        )
    if staff_id_filter:
        leave_records = leave_records.filter(staff_id__id__icontains=staff_id_filter)
    if start_date_filter:
        leave_records = leave_records.filter(start__gte=start_date_filter)
    if end_date_filter:
        leave_records = leave_records.filter(end__lte=end_date_filter)
    paginator = Paginator(leave_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'leave_list': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'staff_id_filter': staff_id_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    }
    return render(request, 'staff/staff_leave_list.html', context)


def staff_attendance(request):
    staffs = StaffMaster.objects.all()  # Fetch all staff records
    today = date.today().strftime('%Y-%m-%d')  # Get today's date

    if request.method == 'POST':
        form = StaffAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)  # Don't commit yet
            try:
                attendance.submitted_by = request.user 
                attendance.date = today
                attendance.save()
                
                messages.success(request, 'Attendance submitted successfully!')
                return redirect('staff_attendance_list')
            except StaffMaster.DoesNotExist:
                form.add_error(None, 'Staff record for the selected user does not exist.')
        else:
            print(form.errors)
    else:
        form = StaffAttendanceForm(initial={'date': today})  # Prepopulate the date field

    return render(request, 'staff/staff-attendance.html', {'form': form, 'today': today, 'staffs': staffs})

def update_attendance_status(request, pk, status):
    # Check if the user has the 'principal' role
    if not hasattr(request.user, 'staffmaster') or request.user.staffmaster.role != 'principal':
        raise PermissionDenied("You do not have permission to update attendance.")

    attendance_record = get_object_or_404(StaffAttendance, pk=pk)
    if status in ['Present', 'Absent']:
        # Update the attendance status
        attendance_record.status = status
       
        attendance_record.save()

        # Send an email notification
        staff_member_email = attendance_record.staff_id.email  # Assuming you have an email field
        user_email = request.user.email  # Email of the principal who updated the status
        subject = f'Attendance Status Updated for {attendance_record.staff_id}'
        message = (
            f'Dear {attendance_record.staff_id.name},\n\n'
            f'The attendance status for {attendance_record.date} has been updated to {status} by {request.user.username}.\n\n'
            f'Best regards,\n'
            f'The College Management Team'
        )
        send_mail(subject, message, user_email, [staff_member_email])

        messages.success(request, f'Attendance status updated to {status}.')
    else:
        messages.error(request, 'Invalid status.')

    return redirect('staff_attendance_list')



def staff_leave(request):
    staffs = StaffMaster.objects.all()
    if request.method == 'POST':
        form = StaffLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            try:
                staff = StaffMaster.objects.get(user=request.user)
                leave.staff_id = staff  # Assign the StaffMaster instance
                leave.save()
                send_mail(
                    subject=f'Leave Status of {leave.staff_id.name} ',  # Simplified subject line
                    message=f'Dear {leave.staff_id.name},\n\n'
                            f'The attendance status for {leave.start} to {leave.end} has been in {leave.status} status.\n\n'
                            'Best regards,\nThe College Management Team',
                    from_email=None,  # Specify a sender email if needed
                    recipient_list=[staff.email],
                    fail_silently=False,
                )
                messages.success(request, 'Attendance submitted successfully!')
                return redirect('staff_leave_list')
            except StaffMaster.DoesNotExist:
                form.add_error(None, 'Staff record for the logged-in user does not exist.')
    else:
        form = StaffLeaveForm()

    return render(request, 'staff/staff-leave.html', {'form': form, 'staffs': staffs})


def staff_leave_update(request, pk):
    staffs = StaffMaster.objects.all()
    staff_leave = get_object_or_404(StaffLeave, pk=pk)
    if request.method == 'POST':
        form = StaffLeaveForm(request.POST, instance=staff_leave)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('staff_leave_list')  
    else:
        form = StaffLeaveForm(instance=staff_leave)
    return render(request, 'staff/leave-edit.html', {'form': form,'staffs':staffs})

def update_leave_status(request, leave_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        leave = get_object_or_404(StaffLeave, id=leave_id)
        
        if status in dict(StaffLeave.status_choices).keys():
            leave.status = status
            if status in ['Approved', 'rejected']:
                leave.approved_by = request.user  # Update the approved_by field
                leave.save()

                # Send an email notification
                staff_member_email = leave.staff_id.email  # Assuming you have an email field
                user_email = request.user.email  # Email of the principal who updated the status
                subject = f'Leave Status Updated for {leave.staff_id.name}'
                message = (
                        f'Dear {leave.staff_id.name},\n\n'
                        f'The leave status for {leave.start} to {leave.end} has been updated to {status} by {request.user.username}.\n\n'
                        f'Best regards,\n'
                        f'The College Management Team'
                    )
                send_mail(subject, message, user_email, [staff_member_email])
            else:
                leave.save()
                messages.success(request, 'Leave status updated successfully!')
        else:
            messages.error(request, 'Invalid status!')
    
    return redirect('staff_leave_list')

def staff_toggle_status(request, pk):
    staff = get_object_or_404(StaffMaster, pk=pk)
    staff.status = False
    staff.save()

    messages.success(request, f'{staff.name} has been deactivated successfully.')
    return redirect('staff_list')

