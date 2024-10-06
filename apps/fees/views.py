import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import FeesMaster, FeesStructure
from .forms import FeesMasterForm, FeesStructureForm 
from apps.course.models import CourseMaster
from apps.student.models import StudentMaster,StudentDetails
from django.contrib import messages
from django.db.models import Q
from apps.course.models import CourseMaster, DivisionMaster
from apps.subject.models import SyllabusMaster
import openpyxl
from django.core.paginator import Paginator


def fees_dash(request):
    return render(request,'dashboard.html') 

def fees_list(request):
    course_id = request.GET.get('course_id', '')
    selected_year = request.GET.get('year', '')
    search_query = request.GET.get('search', '')
    fees = FeesMaster.objects.all()

    # Apply filters based on user input
    if course_id:
        fees = fees.filter(course_id=course_id)
    if search_query:
        search_filters = Q()
        search_fields = ['id', 'amount', 'remaining_amount', 'fees_type', 'status', 'payment_type']
        foreign_key_fields = {
            'course__name': 'course',
            'student__first_name': 'student',
            'student__middle_name': 'student', 
            'student__last_name': 'student', 
            'submitted_by__username': 'submitted_by'
        }
        for field in search_fields:
            search_filters |= Q(**{f"{field}__icontains": search_query})
        for field, related_model in foreign_key_fields.items():
            search_filters |= Q(**{f"{field}__icontains": search_query})
        fees = fees.filter(search_filters)

    if selected_year:
        fees = fees.filter(year=selected_year)

    try:
        if search_query:
            amount_value = float(search_query)
            fees = fees.filter(Q(amount=amount_value) | Q(remaining_amount=amount_value))
    except ValueError:
        pass

    # Check if the export button was clicked
    if 'export' in request.GET:
        return export_to_excel_fees(fees) 
     
    courses = CourseMaster.objects.all()
    years = SyllabusMaster.objects.values_list('year', flat=True).distinct()

    return render(request, 'fees/fees_list.html', {
        'fees': fees,
        'courses': courses,
        'years': years,
        'selected_course': course_id,
        'selected_year': selected_year,
        'search_query': search_query
    })


def export_to_excel_fees(fees):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Fees Data'

    # Define the headers
    headers = ['ID', 'Student ID', 'Course', 'Year', 'Amount', 'Remaining Amount', 'Date', 'Payment Type', 'Status', 'Submitted By']
    worksheet.append(headers)

    # Write data to the Excel sheet
    for fee in fees:
        worksheet.append([
            fee.pk,
            f"{fee.student.first_name} {fee.student.middle_name} {fee.student.last_name}",
            fee.course.name,
            fee.year,
            fee.amount,
            fee.remaining_amount,
            fee.date,
            fee.payment_type,
            fee.status,
            fee.submitted_by.username if fee.submitted_by else 'N/A',
        ])
    
    # Create the response to return the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=fees_data.xlsx'

    # Save the workbook to the response
    workbook.save(response)  
    return response

def fees_detail(request, pk):
    fees = get_object_or_404(FeesMaster, pk=pk)
    return render(request, 'fees/fees_detail.html', {'fees': fees})

def fees_create(request):
    # Fetch all courses, students, and fees structures
    courses = CourseMaster.objects.all() 
    students = StudentMaster.objects.all()
    feesstructures = FeesStructure.objects.all()
    
    if request.method == 'POST':
        form = FeesMasterForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.cleaned_data['student']
            fees_structure = form.cleaned_data['fees_structure']
            entered_amount = form.cleaned_data['amount']
            
            # Fetch the previous fees entry for the student and fees structure
            previous_fees = FeesMaster.objects.filter(student=student, fees_structure=fees_structure).order_by('-id').first()
            
            if previous_fees:
                # Existing fees record found
                if previous_fees.remaining_amount == 0:
                    messages.error(request, 'Your fees are complete for this year. You cannot submit additional fees.')
                    return redirect('fees_list')
                
                previous_remaining_amount = previous_fees.remaining_amount
                total_remaining = previous_remaining_amount - entered_amount
                
                if entered_amount > previous_remaining_amount:
                    messages.error(request, 'Entered amount is greater than the remaining fees amount.')
                else:
                    # Create a new fees entry based on the existing record
                    fees_instance = form.save(commit=False)
                    fees_instance.remaining_amount = total_remaining
                    
                    # Use existing course and year from previous record
                    fees_instance.course = previous_fees.course  
                    fees_instance.year = previous_fees.year      
                    
                    # Store the logged-in user as the one who submitted the fees
                    fees_instance.submitted_by = request.user  
                    
                    fees_instance.save()
                    
                    if total_remaining == 0:
                        messages.success(request, 'Fees submitted successfully! Your fees are complete for this year.')
                    else:
                        messages.success(request, f'Fees submitted successfully! Remaining amount to be paid: {total_remaining}.')
                    return redirect('fees_list')
            else:
                # Handle case where no previous fees record exists
                fees_instance = form.save(commit=False)
                fees_instance.remaining_amount = form.cleaned_data['fees_structure'].amount - entered_amount  # Deduct from selected fees structure
                
                # Use course and year from the form
                fees_instance.course = form.cleaned_data['course']
                fees_instance.year = form.cleaned_data['year']  
                
                # Store the logged-in user as the one who submitted the fees
                fees_instance.submitted_by = request.user
                
                fees_instance.save()
                messages.success(request, 'Fees submitted successfully! This is the first payment for this fees structure.')
                return redirect('fees_list')
        else:
            print(form.errors)  # Debugging purposes, can be removed in production
    else:
        form = FeesMasterForm()

    context = {
        'form': form,
        'courses': courses,
        'feesstructures': feesstructures,
        'students': students
    }
    return render(request, 'fees/fees.html', context)


#------------------------------------------------------------------------------------------------------------------------------------


def fetch_students(request):
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')

    if not course_id or not year:
        return JsonResponse({'error': 'Invalid course or year provided.'}, status=400)

    students = StudentDetails.objects.filter(course_id=course_id, year=year).select_related('student')
    
    if not students.exists():
        return JsonResponse('<option value="" disabled selected>No students found</option>', safe=False)

    student_options = '<option value="" disabled selected>Select student</option>'
    for student_detail in students:
        student = student_detail.student
        student_options += f'<option value="{student.id}">{student.first_name} {student.middle_name} {student.last_name}</option>'

    return JsonResponse(student_options, safe=False)
#------------------------------------------------------------------------------------------------------------------------------------

def fees_update(request, pk):
    courses = CourseMaster.objects.all()
    students = StudentMaster.objects.all()
    feesstructures = FeesStructure.objects.all()
    fee = get_object_or_404(FeesMaster, pk=pk)

    if request.method == 'POST':
        form = FeesMasterForm(request.POST, request.FILES, instance=fee)
        if form.is_valid():
            student = form.cleaned_data['student']
            fees_structure = form.cleaned_data['fees_structure']
            entered_amount = form.cleaned_data['amount']

            # Fetch the previous fees entry for the student and fees structure (excluding the current one)
            previous_fees = FeesMaster.objects.filter(student=student, fees_structure=fees_structure).exclude(pk=pk).order_by('-id').first()

            if previous_fees:
                # If an existing record is found
                if previous_fees.remaining_amount == 0:
                    messages.error(request, 'Your fees are complete for this year. You cannot submit additional fees.')
                    return redirect('fees_detail', pk=fee.pk)

                previous_remaining_amount = previous_fees.remaining_amount
                total_remaining = previous_remaining_amount - entered_amount

                if entered_amount > previous_remaining_amount:
                    messages.error(request, 'Entered amount is greater than the remaining fees amount.')
                else:
                    # Update the current fee entry
                    fee.remaining_amount = total_remaining
                    fee.course = previous_fees.course  # Use existing course from previous record
                    fee.year = previous_fees.year      # Use existing year from previous record
                    fee.submitted_by = request.user    # Update the user who submitted the fees
                    fee.save()

                    if total_remaining == 0:
                        messages.success(request, 'Fees updated successfully! Your fees are complete for this year.')
                    else:
                        messages.success(request, f'Fees updated successfully! Remaining amount to be paid: {total_remaining}.')
                    return redirect('fees_detail', pk=fee.pk)
            else:
                # Handle the case where no previous fees record exists
                fee.remaining_amount = fees_structure.amount - entered_amount  # Deduct from selected fees structure
                fee.course = form.cleaned_data['course']
                fee.year = form.cleaned_data['year']
                fee.submitted_by = request.user
                fee.save()
                messages.success(request, 'Fees updated successfully! This is the first payment for this fees structure.')
                return redirect('fees_detail', pk=fee.pk)
        else:
            print(form.errors)  # Debugging purposes, can be removed in production
    else:
        form = FeesMasterForm(instance=fee)

    context = {
        'form': form,
        'structures': feesstructures,
        'courses': courses,
        'students': students,
    }
    return render(request, 'fees/fees_form.html', context)

def fees_structure_list(request):
    course_id = request.GET.get('course', '')
    year = request.GET.get('year', '')
    search_query = request.GET.get('search', '')

    fees_structures = FeesStructure.objects.all()

    # Filtering based on course and year
    if course_id:
        fees_structures = fees_structures.filter(course_id=course_id)

    if year:
        fees_structures = fees_structures.filter(year=year)

    # Search functionality
    if search_query:
        search_filters = Q()
        search_fields = ['cast', 'name', 'is_gap']
        for field in search_fields:
            search_filters |= Q(**{f"{field}__icontains": search_query})

        foreign_key_fields = {
            'course_id__name': 'course',
        }
        for field, related_model in foreign_key_fields.items():
            search_filters |= Q(**{f"{field}__icontains": search_query})

        try:
            amount_value = float(search_query)
            search_filters |= Q(amount=amount_value)
        except ValueError:
            pass

        fees_structures = fees_structures.filter(search_filters)

    # Adding pagination
    paginator = Paginator(fees_structures, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = CourseMaster.objects.all()

    return render(request, 'fees/fees_structure_list.html', {
        'page_obj': page_obj,
        'fees_structures': page_obj.object_list,
        'courses': courses,
        'search_query': search_query,
    })
def fees_structure_detail(request, pk):
    fees_structure = get_object_or_404(FeesStructure, pk=pk)
    return render(request, 'fees/fees_structure_detail.html', {'fees_structure': fees_structure})

def fees_structure_create(request):
    
    courses=CourseMaster.objects.all()
    if request.method == 'POST':
        form = FeesStructureForm(request.POST)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('fees_structure_list')
    else:
        form = FeesStructureForm()
    contex={'form': form,'courses':courses,}
    return render(request, 'fees/fees-structure.html',contex)



def fees_structure_update(request, pk):
    courses = CourseMaster.objects.all() 
    fees_structure = get_object_or_404(FeesStructure, id=pk)  

    if request.method == 'POST':
        form = FeesStructureForm(request.POST, instance=fees_structure)
        if form.is_valid():
            print(form.data)
            form.save()
            return redirect('fees_structure_list')
    else:
        form = FeesStructureForm(instance=fees_structure)
    
    return render(request, 'fees/fees_structure_form.html', {
        'form': form,
        'courses': courses,
        'fees_structure': fees_structure,
    })

 
def fees_Structure_delete(request, pk):
    Fees = get_object_or_404(FeesStructure, pk=pk)
    if request.method == "POST":
        Fees.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('fees_structure_list') 
    
def toggle_fees_structure_status(request, pk):
    fees_structure = get_object_or_404(FeesStructure, pk=pk)
    if fees_structure.status == 'active':
        fees_structure.status = 'inactive'
        messages.success(request, f"Fees Structure '{fees_structure.name}' has been deactivated.")
    else:
        fees_structure.status = 'active'
        messages.success(request, f"Fees Structure '{fees_structure.name}' has been activated.")
    fees_structure.save()
    return redirect('fees_structure_list')