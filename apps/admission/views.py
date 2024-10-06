from django.shortcuts import render, get_object_or_404, redirect
from .models import AdmissionMaster
from .forms import AdmissionMasterForm
from apps.fees.models import FeesStructure
from apps.course.models import CourseMaster
from apps.student.models import StudentMaster
from django.contrib import messages

def admission_list(request):
    admissions = AdmissionMaster.objects.all()
    return render(request, 'admission/admission_list.html', {'admissions': admissions})

def admission_detail(request, pk):
    admission = get_object_or_404(AdmissionMaster, id=pk)
    return render(request, 'admission/admission_detail.html', {'admission': admission})

def admission_create(request):
    fesses = FeesStructure.objects.all()
    students = StudentMaster.objects.all()
    courses = CourseMaster.objects.all()

    if request.method == 'POST':
        form = AdmissionMasterForm(request.POST, request.FILES)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            admissionby=form.save(commit=False)
            admissionby.admission_by = request.user
            admissionby.save()   
            print(admissionby)
            return redirect('admission_list')
    else:
        form = AdmissionMasterForm()

    contex ={
        'form': form,
        'fesses': fesses,
        'students': students,
        'courses': courses,
    }
    return render(request, 'admission/addmission.html',contex)

def admission_update(request, pk):
    fesses = FeesStructure.objects.all()
    students = StudentMaster.objects.all()
    courses = CourseMaster.objects.all()
    admission = get_object_or_404(AdmissionMaster, pk=pk)
    if request.method == 'POST':
        form = AdmissionMasterForm(request.POST, request.FILES, instance=admission)
        if form.is_valid():
            form.save()
            messages.success(request, 'admission details have been updated successfully.')
            return redirect('admission_list')
    else:
        form = AdmissionMasterForm(instance=admission)

    contex ={
        'form': form,
        'fesses': fesses,
        'students': students,
        'courses': courses,
    }
    return render(request, 'admission/admission_form.html',contex)
