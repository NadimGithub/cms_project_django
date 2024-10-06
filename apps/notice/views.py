from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import NoticeMaster
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import NoticeMasterForm
from django.contrib import messages

def notice_dash(request):

    return render(request,'dashboard.html') 


def update_notice_status():
    today = timezone.now().date()
    expired_notices = NoticeMaster.objects.filter(date_of_end__lt=today, status='active')
    print(f"Updating {expired_notices.count()} notices to inactive")
    expired_notices.update(status='inactive')
    
def notice_list(request):
    notices = NoticeMaster.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    query = request.GET.get('q')

    if start_date and end_date:
        notices = notices.filter(date_of_end__range=[start_date, end_date])  # Change 'deadline' to 'date_of_end'

    if query:
        notices = notices.filter(
            Q(title__icontains=query) | 
            Q(status__icontains=query) |
            Q(notice_type__icontains=query)
        )

    # Pagination
    paginator = Paginator(notices, 10)  # Show 10 notices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'notice/notice_list.html', { 
        'end_date': end_date,
        'start_date': start_date,
        'page_obj': page_obj,
        'query': query,
    })

def notice_detail(request, pk):
    notice = get_object_or_404(NoticeMaster, pk=pk)
    return render(request, 'notice/notice_detail.html', {'notice': notice})

def notice_create(request):
    if request.method == 'POST':
        form = NoticeMasterForm(request.POST)
        print(form.data)
        print(form.errors)
        
        if form.is_valid():
            notice = form.save(commit=False)  # Do not save to DB yet
            notice.submitted_by = request.user # Store the username of the logged-in user
            notice.save()  # Now save it to the database
            return redirect('notice_list')  # Redirect after saving
    else:
        form = NoticeMasterForm()  # Render a blank form for GET requests
    
    return render(request, 'notice/notice.html', {'form': form})

def notice_delete(request, pk):
    notice = get_object_or_404(NoticeMaster, pk=pk)
    if request.method == "POST":
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')  # Redirect to the list of no


def notice_update(request, pk):
    # Retrieve the specific notice object
    notice = get_object_or_404(NoticeMaster, id=pk)

    if request.method == 'POST':
      
        form = NoticeMasterForm(request.POST, instance=notice)
        print("Form data received =", form.data)   
        
        if form.is_valid():
        
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notice_list')
        else:
            
            print("Form errors =", form.errors)  
    else:
       
        form = NoticeMasterForm(instance=notice)
        print("Form initialized with instance data:", form.data)   

     
    return render(request, 'notice/notice_form.html', {'form': form})