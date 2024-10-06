from decimal import Decimal, InvalidOperation
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
import openpyxl
from apps.staff.views import export_attendance_to_excel
from .models import ExamPaper, Result
from .forms import  ExamPaperForm, ResultForm
from apps.course.models import CourseMaster, DivisionMaster
from apps.subject.models import SubjectMaster
from apps.student.models import StudentDetails, StudentMaster
from apps.staff.models import StaffMaster
from apps.institute.models import InstituteMaster
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import json

def exam_dash(request):
    return render(request,'dashboard.html') 

#------------------------------------------------------------------------------------------------------------------------------------
def fetch_years(request):
    print("function call of exam of year")
    course_id = request.GET.get('course_id')
    divisions = DivisionMaster.objects.filter(course_id=course_id).values('year', 'semester').distinct()
    
    # Extract years from the queryset
    years = [div['year'] for div in divisions if 'year' in div]
    
    options = '<option value="" disabled selected>Select year</option>'
    for year in years:
        options += f'<option value="{year}">{year}</option>'
    
    return JsonResponse(options, safe=False)


def fetch_semesters(request):
    print("function call of exam of semistar")
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    divisions = DivisionMaster.objects.filter(course_id=course_id, year=year).values('semester').distinct()
    semesters = [div['semester'] for div in divisions]
    options = '<option value="" disabled selected>Select semester</option>'
    for semester in semesters:
        options += f'<option value="{semester}">{semester}</option>'
    return JsonResponse(options, safe=False)

def fetch_divisions(request):
    print("function call of exam division")
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    divisions = DivisionMaster.objects.filter(course_id=course_id, year=year, semester=semester).values('id', 'name')
    options = '<option value="" disabled selected>Select division</option>'
    for division in divisions:
        options += f'<option value="{division["id"]}">{division["name"]}</option>'
    
    return JsonResponse(options, safe=False)
def fetch_subjects(request):
    course_id = request.GET.get('course_id')
    subjects = SubjectMaster.objects.filter(course_id=course_id)
    response_html = ''.join([f'<option value="{subject.id}">{subject.name}</option>' for subject in subjects])
    return JsonResponse(response_html, safe=False)

#------------------------------------------------------------------------------------------------------------------------------------


def exam_paper_list(request):
    subject_id = request.GET.get('subject', '')  # Get selected subject ID
    course_id = request.GET.get('course_id', '')  # Get selected course ID
    selected_year = request.GET.get('year', '')  # Get selected year
    semester = request.GET.get('semester', '')  # Get selected semester
    search_query = request.GET.get('q', '')  # Get search query

    # Get all exam papers
    exampapers = ExamPaper.objects.all()

    # Filter by course
    if course_id:
        exampapers = exampapers.filter(course__id=course_id)

    # Filter by year
    if selected_year:
        exampapers = exampapers.filter(year=selected_year)


    if subject_id:
        exampapers = exampapers.filter(subject__id=subject_id)

    # Search functionality (search across multiple fields)
    if search_query:
        exampapers = exampapers.filter(
            Q(id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(course__name__icontains=search_query) |
            Q(subject__name__icontains=search_query) |
            Q(staff__name__icontains=search_query)
        )

    # Paginate the result (10 per page)
    paginator = Paginator(exampapers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all subjects, courses, and distinct years for the filters
    subjects = SubjectMaster.objects.all()
    courses = CourseMaster.objects.all()
    years = ExamPaper.objects.values_list('year', flat=True).distinct()  # Use distinct years from ExamPaper

    # Get distinct semesters based on the selected year


    # Pass the selected values back to the template for persistence
    context = {
        'selected_subject': subject_id,
        'selected_course': course_id,
        'selected_year': selected_year,
        'selected_semester': semester,
        'subjects': subjects,
        'courses': courses,
        'years': years,
        
        'exampaper': page_obj,
        'search_query': search_query,
    }

    return render(request, 'exam/exam_paper_list.html', context)



def update_exam_status(request, exam_id):
    if request.method == 'POST':
        status = request.POST.get('status')  # Get status from the form
        exam_paper = get_object_or_404(ExamPaper, id=exam_id)  # Fetch the exam paper

        # Retrieve available status choices from the model
        status_choices = dict(ExamPaper.STATUS_CHOICES)

        # Check if the provided status is valid
        if status in status_choices:
            exam_paper.status = status
            exam_paper.save()  # Save the updated status
            messages.success(request, 'Exam status updated successfully!')
        else:
            messages.error(request, 'Invalid status!')
    else:
        messages.error(request, 'Invalid request method!')

    return redirect('exam_paper_list')

def result_detail(request, pk):
    result = get_object_or_404(Result, pk=pk)
    return render(request, 'exam/result_detail.html', {'result': result})


def exam_paper_view(request, pk=None):
    exam_paper = get_object_or_404(ExamPaper, pk=pk)
    context = {
        'exam_paper': exam_paper,  # Pass the ExamPaper object itself
        'questions': exam_paper.questions,  # Pass the questions list from the JSON field
        'institute': InstituteMaster.objects.all(),  # Adjust according to your actual model
    }
    return render(request, 'exam/exam-paper-view.html', context)

def exam_paper_create(request):
    subjects = SubjectMaster.objects.all()
    staffs = StaffMaster.objects.all()
    courses = CourseMaster.objects.all()

    if request.method == 'POST':
        exam_paper_form = ExamPaperForm(request.POST)
        print(exam_paper_form.data)
        print(exam_paper_form.errors)

        if exam_paper_form.is_valid():
            # Extract question data from the request
            question_nos = request.POST.getlist('question_no')
            question_texts = request.POST.getlist('question_text')
            question_marks = request.POST.getlist('question_marks')

            # Combine the question data into a list of dictionaries
            questions = []
            for question_no, question_text, question_mark in zip(question_nos, question_texts, question_marks):
                questions.append({
                    'question_no': question_no,
                    'question_text': question_text,
                    'question_marks': question_mark
                })

            # Save the ExamPaper instance with questions
            exam_paper = exam_paper_form.save(commit=False)
            exam_paper.questions = questions  # Manually set the questions field
            exam_paper.save()
            
            return redirect('exam_paper_list')

    else:
        exam_paper_form = ExamPaperForm()

    context = {
        'exam_paper_form': exam_paper_form,
        'subjects': subjects,
        'staffs': staffs,
        
        'courses': courses,
    }
    return render(request, 'exam/exam_paper_form.html', context)


def edit_exam_paper(request, exam_paper_id):
    exam_paper = get_object_or_404(ExamPaper, id=exam_paper_id)
    
    # Fetch related data for dropdowns
    courses = CourseMaster.objects.all()
    subjects = SubjectMaster.objects.all()
    staffs = StaffMaster.objects.all()

    if request.method == 'POST':
        # Handle POST request to save the form
        # Update the ExamPaper object
        exam_paper.name = request.POST.get('name')
        exam_paper.course_id = request.POST.get('course')
        exam_paper.year = request.POST.get('year')
        exam_paper.semester = request.POST.get('semester')
        exam_paper.division = request.POST.get('division')
        exam_paper.subject_id = request.POST.get('subject')
        exam_paper.staff_id = request.POST.get('staff')
        exam_paper.total_marks = request.POST.get('total_marks')
        exam_paper.date = request.POST.get('date')
        exam_paper.time = request.POST.get('time')
        exam_paper.duration = request.POST.get('duration')
        exam_paper.location = request.POST.get('location')
        exam_paper.type = request.POST.get('type')
        exam_paper.instructions = request.POST.get('instructions')

        # Collect question data from the form
        questions = []
        question_nos = request.POST.getlist('question_no')
        question_texts = request.POST.getlist('question_text')
        question_marks = request.POST.getlist('question_marks')

        for no, text, marks in zip(question_nos, question_texts, question_marks):
            questions.append({
                'question_no': no,
                'question_text': text,
                'question_marks': marks
            })

        # Save questions in JSONField
        exam_paper.questions = questions
        exam_paper.save()

        # Redirect after saving
        return redirect('exam_paper_list')

    # Pass context to the template, including existing questions
    context = {
        'exam_paper': exam_paper,
        'courses': courses,
        'subjects': subjects,
        'staffs': staffs,
        'questions': exam_paper.questions,  # Directly use the questions JSON data
    }

    return render(request, 'exam/exam-paper-edit.html', context)



def result_create(request):
    exams = ExamPaper.objects.all()
    students = StudentMaster.objects.all()
    subjects = SubjectMaster.objects.all()
    courses = CourseMaster.objects.all()

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            # Retrieve data from form but do not save yet
            result_data = form.cleaned_data

            # Iterate over students to handle the student-specific fields
            for student in students:
                std_id_field = f'std_id_{student.id}'
                marks_field = f'marks{student.id}'

                # Make sure both std_id and marks fields are present in POST data
                if std_id_field in request.POST and marks_field in request.POST:
                    student_id = request.POST.get(std_id_field)
                    marks = request.POST.get(marks_field)

                    if marks:  # Ensure marks is not empty
                        try:
                            marks_value = float(marks)  # Convert to a float (for DecimalField)

                            # Create a Result entry for each student
                            Result.objects.create(
                                exam=result_data['exam'],
                                std_id=StudentMaster.objects.get(pk=student_id),
                                year=result_data['year'],
                                semester=result_data['semester'],
                                division=result_data['division'],
                                subject=result_data['subject'],
                                marks=marks_value,
                                course_id=result_data['course_id']
                            )
                        except ValueError:
                            print(f"Invalid marks value for student {student_id}: {marks}")
                        except IntegrityError as e:
                            print(f"Integrity error for student {student_id}: {e}")
                        except Exception as e:
                            print(f"Error saving data for student {student_id}: {e}")

            return redirect('result_list')  # Redirect after successful submission
        else:
            print("Form Errors:", form.errors)

    else:
        form = ResultForm()

    context = {
        'form': form,
        'students': students,
        'courses': courses,
        'subjects': subjects,
        'exams': exams,
    }

    return render(request, 'exam/add-result.html', context)

#------------------------------------------------------------------------------------------------------------------------------------


def fetch_students_result(request):
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

    return JsonResponse({'students': student_list})

def fetch_exams(request):
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    
    # Fetch exams related to the selected course, year, and semester
    exams = ExamPaper.objects.filter(course_id=course_id, year=year, semester=semester)
    
    exam_list = [{"id": exam.id, "name": exam.name} for exam in exams]
    
    return JsonResponse({'exams': exam_list})
    
#------------------------------------------------------------------------------------------------------------------------------------

def result_update(request, pk):
    # Fetching all required data
    exams = ExamPaper.objects.all()
    students = StudentMaster.objects.all()
    courses = CourseMaster.objects.all()
    subjects = SubjectMaster.objects.all()
    
    # Fetching the specific Result instance
    result = get_object_or_404(Result, pk=pk)

    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result, is_update=True)  # Pass is_update as True
        print("Data Submitted:", request.POST)
        print("Form Errors:", form.errors)
        print("Form Data:", form.data)

        if form.is_valid():
            form.save()  # Save the form to update the result instance
            return redirect('result_list')  # Redirect to your results list page
        else:
            print("Form is not valid!")  # Print if the form fails validation
    else:
        form = ResultForm(instance=result, is_update=True)  # Ensure it shows the current data for update

    # Preparing context for the template
    context = {
        'form': form,
        'students': students,
        'courses': courses,
        'subjects': subjects,
        'exams': exams,
        'result': result,
    }
    
    return render(request, 'exam/edit-result.html', context)



def result_list(request):
    courses = CourseMaster.objects.all()
    query = request.GET.get('q')

    # Initialize filters based on request parameters
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    division = request.GET.get('division')
    subject = request.GET.get('subject')

    # Start with all results
    results = Result.objects.all()

    # Apply filters only if they are provided
    if course_id or year or semester or division or subject or query: 
        if course_id:
            results = results.filter(course_id_id=course_id)
        if year:
            results = results.filter(year=year)
        if semester:
            results = results.filter(semester=semester)
        if division:
            results = results.filter(division=division)
        if subject:
            results = results.filter(subject_id=subject)

        # Initialize filters as an empty Q object
        filters = Q()

        # Search functionality
        if query:
            filters |= Q(std_id__first_name__icontains=query) | \
                       Q(exam__name__icontains=query) | \
                       Q(subject__name__icontains=query) | \
                       Q(division__icontains=query) | \
                       Q(semester__icontains=query) | \
                       Q(year__icontains=query)
            results = results.filter(filters)

    # Check if the "Export" button was clicked
    if 'export' in request.GET:
        return export_results(results)

    # Pagination functionality
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'exam/result_list.html', {
        'courses': courses,
        'page_obj': page_obj,
        'query': query,
        'selected_course_id': course_id,
        'selected_year': year,
        'selected_semester': semester,
        'selected_division': division,
        'selected_subject': subject,
    })

def export_results(results):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Results'

    # Write header
    worksheet.append(['ID', 'Student ID', 'Course', 'Year', 'Semester', 'Division', 'Exam', 'Marks', 'Total Marks'])

    # Write data rows
    for result in results:
        worksheet.append([
            result.pk,
            result.std_id.first_name,
            result.exam.course.name,
            result.year,
            result.semester,
            result.division,
            result.exam.name,
            result.marks,
            result.exam.total_marks,
        ])

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="results.xlsx"'

    workbook.save(response)  # Save the workbook to the response
    return response