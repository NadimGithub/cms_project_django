from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from apps.institute.models import InstituteMaster
from .models import CourseMaster,DivisionMaster
from .forms import CourseMasterForm,DivisionMasterForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def course_dash(request):
    return render(request,'dashboard.html') 

def course_list(request):
    search_query = request.GET.get('q', '')
    course_id = request.GET.get('id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Get all courses
    courses = CourseMaster.objects.all()

    # Filter by search query (search in name, status, intake_capacity)
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) |        # Search by course name
            Q(status__iexact=search_query) |         # Search by status
            Q(intake_capacity__icontains=search_query)  # Search by intake capacity
        )
    
    # Filter by course_id if provided
    if course_id:
        courses = courses.filter(id__icontains=course_id)

    # Filter by start_date if provided
    if start_date:
        courses = courses.filter(start_date__gte=start_date)

    # Filter by end_date if provided
    if end_date:
        courses = courses.filter(start_date__lte=end_date)

    paginator = Paginator(courses, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    # Return filtered courses to the template
    return render(request, 'course/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(CourseMaster, pk=pk)
    return render(request, 'course/course_detail.html', {'course': course})

def course_create(request):
    institute = request.user.inst_id  # Assuming 'institute' is a ForeignKey relation on the User model
    if request.method == 'POST':
        form = CourseMasterForm(request.POST)
        print
        if form.is_valid():
            course = form.save(commit=False)
            course.submitted_by = request.user 
            course.institute_id = institute  # Assign the InstituteMaster instance directly
            course.save()
            messages.success(request, 'Course has been created successfully.')
            return redirect('course_list')
    else:
        form = CourseMasterForm()

    return render(request, 'course/add-course.html', {'form': form, 'inst_id': institute.id})



def course_update(request, pk):
    course = get_object_or_404(CourseMaster, pk=pk)
    inst_id = course.institute_id.id
    inst_name = course.institute_id.name

    if request.method == 'POST':
        form = CourseMasterForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.submitted_by = request.user 
            course.save()
            messages.success(request, 'Course has been updated successfully.')
            return redirect('course_list')
    else:
        form = CourseMasterForm(instance=course)

    return render(request, 'course/course_edit.html',{
        'form': form,
        'inst_id': inst_id,
        'inst_name': inst_name,
        'course': course
    })

def course_toggle_status(request, pk):
    course = get_object_or_404(CourseMaster, pk=pk)
    # Toggle the status
    if course.status == 'active':
        course.status = 'inactive'
    else:
        course.status = 'active'
    
    course.save()
    messages.success(request, f'Course "{course.name}" status updated to {course.status}.')
    return redirect('course_list')


def view_division(request):
    search_query = request.GET.get('q', '')  # Get the search query
    course_query = request.GET.get('course', '')  # Get the course filter
    year_query = request.GET.get('year', '')  # Get the year filter
    semester_query = request.GET.get('semester', '')  # Get the semester filter

    # Start with all divisions
    divisions = DivisionMaster.objects.all()

    # Apply filters based on the GET parameters
    if course_query:
        divisions = divisions.filter(course__name__icontains=course_query)
    if year_query:
        divisions = divisions.filter(year__icontains=year_query)
    if semester_query:
        divisions = divisions.filter(semester__icontains=semester_query)

    # Apply the search query (global search)
    if search_query:
        divisions = divisions.filter(
            Q(name__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(course__name__icontains=search_query) |
            Q(year__icontains=search_query) |
            Q(semester__icontains=search_query)
        )

    # Pagination setup
    paginator = Paginator(divisions, 10)  # Show 10 divisions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'divisions': page_obj,  # Pass the paginated result
        'search_query': search_query,
        'course_query': course_query,
        'year_query': year_query,
        'semester_query': semester_query,
    }
    
    return render(request, 'course/view-division.html', context)

@login_required
def add_division(request):
    courses = CourseMaster.objects.all()
    
    if request.method == 'POST':
        form = DivisionMasterForm(request.POST, request.FILES)
        print(form.errors)  # For debugging purposes, can be removed in production
        
        if form.is_valid():
            # Extract cleaned data from the form
            course = form.cleaned_data['course']
            year = form.cleaned_data['year']
            semester = form.cleaned_data['semester']
            name = form.cleaned_data['name']
            
            if DivisionMaster.objects.filter(course=course, year=year, semester=semester, name=name).exists():
                messages.error(request, 'Division with the same course, year, and semester already exists.')
            else:
                division = form.save(commit=False)
                division.submitted_by = request.user
                division.save()
                messages.success(request, 'Division has been created successfully.')
                return redirect('view_division')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DivisionMasterForm() 

    context = {'form': form, 'courses': courses}
    return render(request, 'course/add-division.html', context)

def division_update(request, pk):
    courses = CourseMaster.objects.all()
    division = get_object_or_404(DivisionMaster, pk=pk)
    if request.method == 'POST':
        form = DivisionMasterForm(request.POST, instance=division)
        if form.is_valid():
                division = form.save(commit=False)
                division.submitted_by = request.user
                division.save()
                messages.success(request, 'division updated successfully!')
                return redirect('view_division')
    else:
        form = DivisionMasterForm(instance=division)
    context = {'form': form, 'courses': courses}
    return render(request, 'course/edit-division.html',context)

