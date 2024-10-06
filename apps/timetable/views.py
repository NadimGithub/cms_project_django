from django.shortcuts import render, get_object_or_404, redirect
from .models import TimetableMaster
from .forms import TimetableForm
from apps.staff.models import StaffMaster
from apps.course.models import CourseMaster
from apps.subject.models import SubjectMaster

# def timetable_dash(request):
#     return render(request,'dashboard.html') 

def timetable_list(request):
    timetables = TimetableMaster.objects.all()
    return render(request, 'timetable/timetable_list.html', {'timetables': timetables})

def timetable_create(request):
    courses = CourseMaster.objects.all()
    staffs= StaffMaster.objects.all()
    subjects= SubjectMaster.objects.all()
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = TimetableForm()
    contex={'form': form,
            'course':courses,
            'staff':staffs,
            'subject':subjects,
            }
    return render(request, 'timetable/timetable.html',contex)

def timetable_detail(request, pk):
    timetables = get_object_or_404(TimetableMaster, pk=pk)
    return render(request, 'timetable/timetable_detail.html', {'timetables': timetables})

def timetable_update(request, pk):
    courses = CourseMaster.objects.all()
    staffs= StaffMaster.objects.all()
    subjects= SubjectMaster.objects.all()
    timetable = TimetableMaster.objects.get(pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = TimetableForm(instance=timetable)
        contex={'form': form,
            'course':courses,
            'staff':staffs,
            'subject':subjects,
            }
    return render(request, 'timetable/timetable_form.html',contex)

def timetable_delete(request, pk):
    timetable = TimetableMaster.objects.get(pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    return render(request, 'timetable/timetable_confirm_delete.html', {'timetable': timetable})
