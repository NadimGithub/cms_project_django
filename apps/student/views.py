from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import StudentMaster, StudentDetails, StudentAttendance, StudentLeave, StudentProgress,TempAddress, PermAddress, Document
from apps.course.models import CourseMaster, DivisionMaster
from apps.staff.models import StaffMaster
from apps.subject.models import SubjectMaster
from apps.accounts.models import CustomUser
from django.contrib import messages 
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .forms import StudentMasterForm, StudentDetailsForm, StudentAttendanceForm, StudentLeaveForm, StudentProgressForm,tempaddressForm,permaddressForm,documentForm
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from datetime import date


def student_dash(request):
    return render(request,'dashboard.html') 

def student_list(request):
    students = StudentMaster.objects.all()
    query = request.GET.get('q')
    if query:
        students = StudentMaster.objects.filter(
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(number__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = StudentMaster.objects.all()
    paginator = Paginator(students, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/student-view.html', {'page_obj': page_obj})


def student_detail(request):
    mobile=request.user.mobile
    student = get_object_or_404(StudentMaster,number=mobile)
    student_details = StudentDetails.objects.filter(student=student).first()
    temp_address = TempAddress.objects.filter(student=student).first()
    perm_address = PermAddress.objects.filter(student=student).first()
    document = Document.objects.filter(student=student)
    context = {
        'student': student,
        'student_details': student_details,
        'temp_address': temp_address,
        'perm_address': perm_address,
        'documents': document,
    }
    return render(request, 'student/student-detail.html', context)


def student_update(request, pk):
    courses = CourseMaster.objects.all() 
    students = get_object_or_404(StudentMaster, pk=pk)
    print('students',students)
    student_details = get_object_or_404(StudentDetails, student=students)
    print('student_details',student_details)
    temp_address = get_object_or_404(TempAddress, student=students)
    print('temp_address',temp_address)
    perm_address = get_object_or_404(PermAddress, student=students)
    print('perm_address',perm_address)

    if request.method == 'POST':
        form = StudentMasterForm(request.POST, request.FILES, instance=students)
        details_form = StudentDetailsForm(request.POST, instance=student_details)
        temp_address_form = tempaddressForm(request.POST, instance=temp_address)
        perm_address_form = permaddressForm(request.POST, instance=perm_address)

        # Exclude the 'student' field when updating
        details_form.fields.pop('student', None)
        temp_address_form.fields.pop('student', None)
        perm_address_form.fields.pop('student', None)

        if all([form.is_valid(), details_form.is_valid(), temp_address_form.is_valid(), perm_address_form.is_valid()]):
            form.save()
            details_form.save()
            temp_address_form.save()
            perm_address_form.save()

            # Send email notification
            # send_mail(
            #     subject='Student Data Updated',
            #     message='Your data has been updated successfully.',
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[students.email],  # Sends the email to the student
            #     fail_silently=False,
            # )
            
            # Optionally add a success message
            messages.success(request, 'Student details have been updated and an email has been sent.')

            return redirect('student_detail', pk=pk)  # Redirect after successful update

    else:
        form = StudentMasterForm(instance=students)
        details_form = StudentDetailsForm(instance=student_details)
        temp_address_form = tempaddressForm(instance=temp_address)
        perm_address_form = permaddressForm(instance=perm_address)

    context = {
        'form': form,
        'details_form': details_form,
        'temp_address_form': temp_address_form,
        'perm_address_form': perm_address_form,
        'courses': courses,
    }

    return render(request, 'student/student-edit.html', context)



def student_delete(request, pk):
    student = get_object_or_404(StudentMaster, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {'student': student})


def student_create(request):

    courses = CourseMaster.objects.all() # Retrieve courses initially
    institute_user = request.user.inst_id

    if request.method == 'POST':
        form = StudentMasterForm(request.POST, request.FILES)
        print(form.data)

        if form.is_valid():
            student = form.save(commit=False)
            student.institute = institute_user
            
            default_password = get_random_string(length=6)
            hashed_password = make_password(default_password)

            if CustomUser.objects.filter(email=student.email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'student/add-student.html', {'form': form, 'courses': courses})

            student.save()

            StudentDetails.objects.create(
                student = student
            )

            TempAddress.objects.create(
                student= student
            )
            PermAddress.objects.create(
                student=student
            )
            user = CustomUser(
                email=student.email,
                username=student.email,
                mobile=student.number,
                password=hashed_password,
                is_staff=True,
                role=student.role,
                first_name=student.first_name,
                inst_id=institute_user  # Set the institute ID here
            )
            user.save()

            profile_image = student.profile_image
            if profile_image:
                image_name = profile_image.name
                image_content = profile_image.read()
                profile_image_file = ContentFile(image_content, image_name)
                user.profile_image.save(image_name, profile_image_file)
                student.user = user
                student.save()

            # Send email notification
            # send_mail(
            #     'Student Created Successfully',
            #     f'Hello {student.first_name},\n\nYour student account has been successfully created.Your password is: {default_password}\n\nPlease log in at: http://127.0.0.1:8000/accounts/login/',
            #     'your-email@example.com',  # From email
            #     [student.email],  # To email
            #     fail_silently=False,
            # )

            messages.success(request, 'Student created successfully and email sent.')
            return redirect('student_create')
        else:
            messages.error(request, 'Form data is invalid.')
            print(form.errors)  # Print form errors if any
    else:
        form = StudentMasterForm()

    context = {'form': form, 'courses': courses}
    return render(request, 'student/add-student.html', context)
#------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------


def student_details_create(request):
    courses = CourseMaster.objects.all()  # Retrieve courses initially
    students = StudentMaster.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')  # Get the selected student

        # Check if the student already has details
        existing_details = StudentDetails.objects.filter(student_id=student_id).first()

        form = StudentDetailsForm(request.POST, request.FILES, instance=existing_details)
        print(form.data)
        print(form.errors)

        if form.is_valid():
            details = form.save(commit=False)
            details.save()
            # subject = 'Student Details Added Successfully'
            # message = (
            #     f'Student {details.student.first_name} {details.student.last_name} '
            #     f'has been added successfully.\n'
            #     f'Parent name: {details.mother_name}\n'
            #     f'DOB: {details.dob}\n'
            #     f'Registration number: {details.registration_number}\n'
            #     f'Blood group: {details.blood_group}\n'
            #     f'Category: {details.category}\n'
            #     f'Caste: {details.caste}\n'
            #     f'Education qualification: {details.education_qualification}\n'
            #     f'Nationality: {details.nationality}\n'
            #     f'Admission type: {details.admission_type}\n'
            #     f'CAP ID: {details.cap_id}/n/n'    
            #     f'Best regards,\nThe College Management Team'    
            # )              
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [details.student.email]  

            # try:
            #     send_mail(subject, message, email_from, recipient_list)
            # except Exception as e:
            #     print(f"Error sending email: {e}")

            # Optionally, you could send an email or perform additional actions here
            return redirect('student_tempaddress')
        else:
            return render(request, 'student/add_student_additional_detail.html', {
                'form': form,
                'students': students,
            })

    else:
        form = StudentDetailsForm()

    return render(request, 'student/add_student_additional_detail.html', {
        'form': form,
        'students': students,
        'courses': courses,
    })


def student_details_update(request, registration_number):
    details = get_object_or_404(StudentDetails, registration_number=registration_number)
    if request.method == 'POST':
        form = StudentDetailsForm(request.POST, request.FILES, instance=details)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=details.student.pk)
    else:
        form = StudentDetailsForm(instance=details)
    return render(request, 'student/.html', {'form': form})

def student_details_delete(request, registration_number):
    details = get_object_or_404(StudentDetails, registration_number=registration_number)
    if request.method == 'POST':
        details.delete()
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {'details': details})

def student_attendance_list(request):
    courses = CourseMaster.objects.all()
    subjects = SubjectMaster.objects.all()
    course_id = request.GET.get('course')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    division = request.GET.get('division')
    subject_id = request.GET.get('subject')
    date = request.GET.get('date')
    search_query = request.GET.get('search')

    # Filtering based on the selected options
    student_attendance = StudentAttendance.objects.all()

    if course_id:
        student_attendance = student_attendance.filter(course=course_id)
    if year:
        student_attendance = student_attendance.filter(year=year)
    if semester:
        student_attendance = student_attendance.filter(semester=semester)
    if division:
        student_attendance = student_attendance.filter(division=division)
    if subject_id:
        student_attendance = student_attendance.filter(subject=subject_id)
    if date:
        student_attendance = student_attendance.filter(date=date)
    if search_query:
        student_attendance = student_attendance.filter(
        Q(student__first_name__icontains=search_query) | 
        Q(student__last_name__icontains=search_query) |
        Q(student__status__icontains=search_query)  # Make sure 'status' is the correct field name
    )
    paginator = Paginator(student_attendance, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'courses': courses,
        'subjects': subjects,
        'students': page_obj,  # Paginated students
        'paginator': paginator,
    }

    return render(request, 'student/student_attendance_list.html', context)

# @login_required
def student_attendance_create(request):
    today = date.today().strftime('%Y-%m-%d')
    courses = CourseMaster.objects.all()
    staff_member = get_object_or_404(StaffMaster, user=request.user)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        division = request.POST.get('division')
        subject_id = request.POST.get('subject')
        students = StudentDetails.objects.filter(
            course_id=course_id,
            year=year,
            semester=semester,
            division=division)
        course = get_object_or_404(CourseMaster, id=course_id)
        for student in students:
            studentID = student.student.id
            attendance_key = f'attendance_{studentID}'
            attendance_status = request.POST.get(attendance_key)
            if attendance_status is not None:
                is_present = attendance_status == 'present'
                StudentAttendance.objects.create(
                    student=student.student,
                    subject_id=subject_id,
                    staff=staff_member,
                    date=today,
                    present=is_present,
                    course=course, 
                    year=year,
                    semester=semester,
                    division=division
                )
        return redirect('student_attendance_list')  
    else:
        students = StudentDetails.objects.all() 
        subjects = SubjectMaster.objects.all()
        context = {
            'today': today,
            'student': students,
            'staff': staff_member,
            'subject': subjects,
            'courses': courses,
        }
    return render(request, 'student/std-attendence.html', context)


def student_attendance_update(request, pk):
    attendance = get_object_or_404(StudentAttendance, pk=pk)  
    if request.method == 'POST':
        form = StudentAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('student_attendance_list')
    else:
        form = StudentAttendanceForm(instance=attendance)
    context = {
        'form': form,
        'attendance': attendance,
        'staff': StaffMaster.objects.all(),
        'subject': SubjectMaster.objects.all(),
        'students': StudentMaster.objects.all(),  
    }
    return render(request, 'student/student-attendance-edit.html', context)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def fetch_students_attendance(request):
    print("function called")
    # Get the parameters from the request
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    division = request.GET.get('division')

    # Debug: Print the received parameters to check if they are correct
    print(f"Course ID: {course_id}, Year: {year}, Semester: {semester}, Division: {division}")

    # Perform filtering on the StudentDetails model (not StudentMaster)
    students = StudentDetails.objects.filter(
        course__id=course_id,  # Use 'course__id' to filter by the course's ID
        year=year,
        semester=semester,
        division=division
    )

    # Debug: Print the list of students to verify if the query is working
    print(f"Fetched students: {students}")

    student_list = []
    for student_detail in students:
        # Access the student field in StudentDetails to get student details
        student_list.append({
            'id': student_detail.student.id,
            'first_name': student_detail.student.first_name,
            'last_name': student_detail.student.last_name,
        })
        print('student list ',student_list)
    return JsonResponse({'students': student_list})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------


def student_attendance_delete(request, pk):
    attendance = get_object_or_404(StudentAttendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('student_attendance_list')
    return render(request, 'student/student_confirm_delete.html', {'attendance': attendance})

def student_leave_list(request):
    leaves = StudentLeave.objects.all()
    return render(request, 'student/student_leave_list.html', {'leaves': leaves})


def student_leave_create(request):
    student = StudentMaster.objects.all()
    if request.method == 'POST':
        form = StudentLeaveForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            leave = form.save(commit=False)
            student = StudentMaster.objects.get(user=request.user)  # Assuming the user is linked to a StudentMaster
            leave.student = student
            leave.save()
            send_mail(
                    subject=f'Leave Status of {leave.student.first_name} ',  # Simplified subject line
                    message=f'Dear {leave.student.first_name},\n\n'
                            f'The attendance status for {leave.start} to {leave.end} has been in {leave.status} status.\n\n'
                            'Best regards,\nThe College Management Team',
                    from_email=None,  # Specify a sender email if needed
                    recipient_list=[student.email],
                    fail_silently=False,
                )
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('student_leave_create')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Error submitting the form.')
    else:
        print("GET request received")
        form = StudentLeaveForm()
    return render(request, 'student/std-leave.html', {'form': form,'student':student})

def student_leave_update(request, pk):
    leave = get_object_or_404(StudentLeave, pk=pk)
    if request.method == 'POST':
        form = StudentLeaveForm(request.POST, instance=leave)
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect('student_leave_list')
    else:
        form = StudentLeaveForm(instance=leave)
    return render(request, 'student/student_leave_form.html', {'form': form})

def student_update_leave_status(request, leave_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        leave = get_object_or_404(StudentLeave, id=leave_id)
        
        if status in dict(StudentLeave.status_choices).keys():
            leave.status = status

            if status in ['Approved', 'rejected']:
                leave.student_approved_by = request.user  # Assign logged-in user
            leave.save()
            staff_member_email = leave.student.email  # Assuming you have an email field
            user_email = request.user.email  # Email of the principal who updated the status
            subject = f'Leave Status Updated for {leave.student.first_name}'
            message = (
                        f'Dear {leave.student.first_name},\n\n'
                        f'The leave status for {leave.start} to  {leave.end} has been updated to {status} by {request.user.username}.\n\n'
                        f'Best regards,\n'
                        f'The College Management Team'
                    )
            send_mail(subject, message, user_email, [staff_member_email])
            messages.success(request, 'Leave status updated successfully!')
        else:
            messages.error(request, 'Invalid status!')
    return redirect('student_leave_list')
# Views for StudentProgress

def student_progress_list(request):
    progress = StudentProgress.objects.all()
    return render(request, 'student/student_progress_list.html', {'progress': progress})

def student_progress_create(request):
    if request.method == 'POST':
        form = StudentProgressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_progress_list')
    else:
        form = StudentProgressForm()
    return render(request, 'student/std-progress.html', {'form': form})

def student_progress_update(request, pk):
    progress = get_object_or_404(StudentProgress, pk=pk)
    if request.method == 'POST':
        form = StudentProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('student_progress_list')
    else:
        form = StudentProgressForm(instance=progress)
    return render(request, 'student/student_progress_form.html', {'form': form})

def student_progress_delete(request, pk):
    progress = get_object_or_404(StudentProgress, pk=pk)
    if request.method == 'POST':
        progress.delete()
        return redirect('student_progress_list')
    return render(request, 'student/student_confirm_delete.html', {'progress': progress})

def student_tempaddress(request):
    student = StudentMaster.objects.all()  # Fetching all students
    staffs = StaffMaster.objects.all()  # Fetching all staff
    
    if request.method == 'POST':
        form = tempaddressForm(request.POST)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            tempaddress = form.save(commit=False)
            tempaddress.save()
            subject = 'Student temporary address details Added Successfully'
            message = (
                f'Student {tempaddress.student.first_name} {tempaddress.student.last_name} '
                f'has been added successfully.\n'
                f'temporary State: {tempaddress.temp_state}\n'
                f'temporary District: {tempaddress.temp_district}\n'
                f'temporary Taluka: {tempaddress.temp_taluka}\n'
                f'temporary City: {tempaddress.temp_city}\n'
                f'temporary Pincode: {tempaddress.temp_pincode}\n'
                f'temporary Address: {tempaddress.temp_address}\n/n'    
                f'Best egards,\nThe College Management Team'    
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [tempaddress.student.email]  
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
               messages.success(request, 'Student  temporary address added successfully.')
            return redirect('student_permaddress')
    else:
        form = tempaddressForm()
    return render(request, 'student/tempaddress.html', {'form': form, 'students': student, 'staffs': staffs})


def student_permaddress(request):
    student = StudentMaster.objects.all() 
    staff = StaffMaster.objects.all()  
    if request.method == 'POST':
        form = permaddressForm(request.POST)
        if form.is_valid():
            permaddress = form.save(commit=False)
            permaddress.save()
            subject = 'Student permanent address details added Successfully'
            message = (
                f'Student {permaddress.student.first_name} {permaddress.student.last_name} '
                f'permanent address added successfully.\n'
                f'permanent State: {permaddress.perm_state}\n'
                f'permanent District: {permaddress.perm_district}\n'
                f'permanent Taluka: {permaddress.perm_taluka}\n'
                f'permanent City: {permaddress.perm_city}\n'
                f'permanent Pincode: {permaddress.perm_pincode}\n'
                f'permanent Address: {permaddress.perm_address}\n/n'    
                f'Best egards,\nThe College Management Team'    
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [permaddress.student.email]  
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
               messages.success(request, 'Student permanent addrress added successfully')
            return redirect('documents')
    else:
        form = permaddressForm()
    return render(request, 'student/permaddress.html', {'form': form, 'students': student, 'staffs': staff})

def Documents(request):
    students = StudentMaster.objects.all()
    staff = StaffMaster.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = StudentMaster.objects.get(id=student_id) if student_id else None

        # Iterate over files if multiple files are sent
        files = request.FILES.getlist('document')
        document_names = request.POST.getlist('document_name')

        if student:
            for doc_file, doc_name in zip(files, document_names):
                document = Document()
                document.student = student
                document.document_uploded = request.user
                document.document_name = doc_name
                document.document = doc_file
                document.save()

                subject = 'Student document added Successfully'
                message = (
                    f'Student {student.first_name} {student.last_name} '
                    f'Your Documents added successfully.\n'    
                    f'Best regards,\nThe College Management Team'    
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [student.email]
                try:
                    send_mail(subject, message, email_from, recipient_list)
                except Exception as e:
                    messages.error(request, f'Error sending email: {e}')

            messages.success(request, 'Documents added successfully')
            return redirect('documents')
        else:
            messages.error(request, 'No student selected')

    else:
        form = documentForm()

    return render(request, 'student/upload_document.html', {'form': form, 'students': students, 'staffs': staff})
def student_toggle_status(request, pk):
    student= get_object_or_404(StudentMaster, pk=pk)
    # Toggle the status
    if student.status == 'active':
        student.status = 'inactive'
    else:
        student.status = 'active'
    
    student.save()
    messages.success(request, f'student "{student.first_name}" status updated to {student.status}.')
    return redirect('student_list')

def attandance_toggle_status(request, pk):
    attandance = get_object_or_404(StudentAttendance, pk=pk)
    attandance.present = not attandance.present  # Toggle the boolean value
    attandance.save()
    status = "Present" if attandance.present else "Absent"
    messages.success(request, f'Student status updated to {status}.')
    return redirect('student_attendance_list')

def update_document(request, student_id):
    student = get_object_or_404(StudentMaster, id=student_id)
    documents = Document.objects.filter(student=student)

    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = student
            document.save()
            messages.success(request, 'Document updated successfully')
            return redirect('documents')  # Adjust the redirect as needed
    else:
        form = documentForm()

    return render(request, 'student/update_document.html', {'form': form, 'student': student, 'documents': documents})

def delete_document(request, document_id):
    document = get_object_or_404(Document, document_id=document_id)  # Ensure you're using the correct field name
    student_id = document.student.id
    print(f"Attempting to delete document with ID: {document_id}")  # Log the document ID for debugging
    document.delete()  # This deletes the document from the database
    messages.success(request, 'Document deleted successfully')
    return redirect('update_document', student_id=student_id)  # Redirect back to the update document page