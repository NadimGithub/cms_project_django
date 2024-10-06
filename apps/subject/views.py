from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import SubjectMaster, SyllabusMaster
from .forms import SubjectMasterForm, SyllabusMasterForm
from apps.course.models import CourseMaster, DivisionMaster
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


def subject_dash(request):
    return render(request,'dashboard.html') 

def subject_list(request):
    course_id = request.GET.get('course_id', '')
    search_query = request.GET.get('search', '')
    selected_year = request.GET.get('year', '')  # Get the selected year from the query params

    subjects = SubjectMaster.objects.all()

    if course_id:
        subjects = subjects.filter(course_id=course_id)

    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) |  # Search by subject name
            Q(type__icontains=search_query) |  # Search by subject type
            Q(course_id__name__icontains=search_query) |  # Search by course name (related field)
            Q(marks_credits__icontains=search_query) |  # Search by marks/credits
            Q(duration__icontains=search_query) |  # Search by duration
            Q(pattern__icontains=search_query) |  # Search by pattern
            Q(submitted_by__username__icontains=search_query)  # Search by submitted by (related field)
        )

    if selected_year:  # Add filtering by year if a year is selected
        subjects = subjects.filter(year=selected_year)

    paginator = Paginator(subjects, 10)
    page_number = request.GET.get('page')
    subjects = paginator.get_page(page_number)
    
    courses = CourseMaster.objects.all()
    years = SubjectMaster.objects.values_list('year', flat=True).distinct()  # Get distinct years

    return render(request, 'subject/subject-list.html', {
        'subjects': subjects,
        'courses': courses,  # Pass courses to the template for the dropdown
        'years': years,  # Pass distinct years to the template for the dropdown
        'selected_course': course_id,  # Pass selected course to keep the filter
        'search_query': search_query,  # Pass search query to keep the search input
        'selected_year': selected_year  # Pass selected year to keep the filter
    })

def subject_detail(request, pk):
    subject = get_object_or_404(SubjectMaster, pk=pk)
    return render(request, 'subject/subject_detail.html', {'subject': subject})

def subject_create(request):
    courses = CourseMaster.objects.all()

    if request.method == 'POST':
        form = SubjectMasterForm(request.POST)
        
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
            name = form.cleaned_data['name']
            year = form.cleaned_data['year']
            semester = form.cleaned_data['semester']
            
            # Check if subject already exists
            if SubjectMaster.objects.filter(course_id=course_id, name=name, year=year, semester=semester).exists():
                messages.error(request, "A subject with the same course, year, semester, and name already exists.")  # Correctly add an error message
            else:
                subject = form.save(commit=False)
                subject.submitted_by = request.user
                subject.save()
                messages.success(request, 'Subject created successfully!')
                return redirect('subject_list')
    else:
        form = SubjectMasterForm()

    context = {'form': form, 'courses': courses}
    return render(request, 'subject/add-subject.html', context)


def subject_update(request, pk):
    courses = CourseMaster.objects.all()
    subject = get_object_or_404(SubjectMaster, pk=pk)
    if request.method == 'POST':
        form = SubjectMasterForm(request.POST, instance=subject)
        print(form.errors)
        if form.is_valid():
            subject=form.save(commit=False)
            subject.submitted_by = request.user
            subject.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('subject_list')
    else:
        form = SubjectMasterForm(instance=subject)
    return render(request, 'subject/subject-edit.html', {'form': form, 'subject': subject,'courses':courses})

def syllabus_list(request):
    subject_id = request.GET.get('subject_id', '')
    course_id = request.GET.get('course_id', '')
    search_query = request.GET.get('search', '')
    selected_year = request.GET.get('year', '')

    syllabuses = SyllabusMaster.objects.all()

    if course_id:
        syllabuses = syllabuses.filter(subject_id__course_id=course_id)

    if search_query:
        syllabuses = syllabuses.filter(
            Q(syllabus_id__icontains=search_query) |
            Q(subject_id__name__icontains=search_query) |
            Q(unit__icontains=search_query) |
            Q(duration__icontains=search_query) |
            Q(marks__icontains=search_query) |
            Q(submitted_by__username__icontains=search_query)
        )

    if selected_year:  # Properly filter syllabuses by selected year
        syllabuses = syllabuses.filter(year=selected_year)

    paginator = Paginator(syllabuses, 10)
    page_number = request.GET.get('page')
    syllabuses = paginator.get_page(page_number)

    subjects = SubjectMaster.objects.all()
    courses = CourseMaster.objects.all()
    years = SubjectMaster.objects.values_list('year', flat=True).distinct()

    return render(request, 'subject/syllabus-view.html', {
        'syllabuses': syllabuses,
        'subjects': subjects,
        'courses': courses,
        'years': years,
        'selected_subject': subject_id,
        'selected_course': course_id,
        'selected_year': selected_year,  # Pass selected year to keep the filter
        'search_query': search_query
    })


def syllabus_detail(request, pk):
    syllabus = get_object_or_404(SyllabusMaster, syllabus_id=pk)
    return render(request, 'subject/syllabus_detail.html', {'syllabus': syllabus})

def syllabus_create(request):
    courses = CourseMaster.objects.all()
    if request.method == 'POST':
        form = SyllabusMasterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
           
            subject_id = form.cleaned_data['subject_id']
            unit = form.cleaned_data['unit']
            points_sub_points = form.cleaned_data['points_sub_points']
            duration = form.cleaned_data['duration']
            marks = form.cleaned_data['marks']

            if SyllabusMaster.objects.filter(
                course_id=course_id,
                subject_id=subject_id,
                unit=unit,
                points_sub_points=points_sub_points,
                duration=duration,
                marks=marks
            ).exists():
                messages.error(request, "A syllabus with the same details already exists.")
            else:
                syllabus = form.save(commit=False)
                syllabus.submitted_by = request.user
                syllabus.save()
                messages.success(request, 'Syllabus created successfully!')
                return redirect('syllabus_list')  # Adjust the redirect to your syllabus list view
        else:
            messages.error(request, "Please correct the errors in the form.")

    else:
        form = SubjectMasterForm()

    context = {'form': form, 'courses': courses}
    return render(request, 'subject/add-syllabus.html', context)

# -----------------------------------------------------ajax call-----------------------------------------------------
def fetch_years(request):
    course_id = request.GET.get('course_id')
    divisions = DivisionMaster.objects.filter(course_id=course_id).values('year', 'semester').distinct()
    
    # Extract years from the queryset
    years = [div['year'] for div in divisions if 'year' in div]
    
    options = '<option value="" disabled selected>Select year</option>'
    for year in years:
        options += f'<option value="{year}">{year}</option>'
    
    return JsonResponse(options, safe=False)


def fetch_semesters(request):
    course_id = request.GET.get('course_id')
    year = request.GET.get('year')
    divisions = DivisionMaster.objects.filter(course_id=course_id, year=year).values('semester').distinct()
    semesters = [div['semester'] for div in divisions]
    options = '<option value="" disabled selected>Select semester</option>'
    for semester in semesters:
        options += f'<option value="{semester}">{semester}</option>'
    return JsonResponse(options, safe=False)


def fetch_subjects(request):
    course_id = request.GET.get('course_id')
    print("Course ID received:", course_id)  # Debug log
    subjects = SubjectMaster.objects.filter(course_id=course_id).values('id', 'name').distinct()
    
    options = '<option value="" disabled selected>Select Subject</option>'
    for subject in subjects:
        options += f'<option value="{subject["id"]}">{subject["name"]}</option>'
    
    print("Options generated:", options)  # Debug log
    return JsonResponse(options, safe=False)

# -----------------------------------------------------ajax call-----------------------------------------------------

def syllabus_update(request, pk):
    courses = CourseMaster.objects.all()
    subjects=SubjectMaster.objects.all()
    syllabus = get_object_or_404(SyllabusMaster, syllabus_id=pk)
    form = SyllabusMasterForm(instance=syllabus)
    if request.method == 'POST':
        form = SyllabusMasterForm(request.POST, instance=syllabus)
        print(form.errors)
        if form.is_valid():
            syllabus=form.save(commit=False)
            syllabus.submitted_by = request.user
            syllabus.save()
            messages.success(request, 'Syllabus updated successfully!')
            return redirect('syllabus_list')
    return render(request, 'subject/syllabus-edit.html', {'form': form, 'syllabus': syllabus,'subjects':subjects,'courses':courses})

def subject_delete(request, pk):
    subject = get_object_or_404(SubjectMaster, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return redirect('subject_list')

def syllabus_delete(request, pk):
    subject = get_object_or_404(SyllabusMaster, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('syllabus_list')
    return redirect('syllabus_list')