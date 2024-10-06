# views.py
from django.shortcuts import render, redirect
from .models import ScholarshipMaster, Document
from .forms import ScholarshipForm

# def scholarship_dash(request):
#     return render(request,'dashboard.html') 

def scholarship_list(request):
    scholarships = ScholarshipMaster.objects.all()
    return render(request, 'scholarship/scholarship_list.html', {'scholarships': scholarships})

def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, request.FILES)
        if form.is_valid():
            scholarship = form.save()
            files = request.FILES.getlist('school_documents')
            for file in files:
                document = Document.objects.create(file=file)
                scholarship.school_documents.add(document)
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'scholarship/scholarship.html', {'form': form})


def scholarship_update(request, pk):
    scholarship = ScholarshipMaster.objects.get(pk=pk)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, request.FILES, instance=scholarship)
        if form.is_valid():
            scholarship = form.save()
            files = request.FILES.getlist('school_documents')
            scholarship.school_documents.clear()
            for file in files:
                document = Document.objects.create(file=file)
                scholarship.school_documents.add(document)
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'scholarship/scholarship_form.html', {'form': form})

def scholarship_delete(request, pk):
    scholarship = ScholarshipMaster.objects.get(pk=pk)
    if request.method == 'POST':
        scholarship.delete()
        return redirect('scholarship_list')
    return render(request, 'scholarship/scholarship_confirm_delete.html', {'scholarship': scholarship})
