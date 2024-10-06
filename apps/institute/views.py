from django.shortcuts import render, get_object_or_404, redirect 
from .models import InstituteMaster
from apps.notice.models import NoticeMaster
from .forms import InstituteMasterForm
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone

def institute_dash(request):
    current_date = timezone.now().date()
    inst_id = request.user.inst_id
    
    notices = NoticeMaster.objects.filter(status='active', date_of_end__gte=current_date).order_by('-date_of_publish')

    
    try:
        inst_id = int(inst_id)
    except (TypeError, ValueError):
        inst_id = None
    
    # Get all institutes or filter by inst_id if user is admin or superuser
    if request.user.is_superuser or request.user.role == 'admin':
        if inst_id is not None:
            institute_name = InstituteMaster.objects.filter(id=inst_id).first()
        else:
            institute_name = None
    else:
   
 
        institute_name = InstituteMaster.objects.all()

    return render(request, 'dashboard.html', {'institute_name': institute_name,'notices': notices})
# def institute_dash(request):
#     inst_id = request.user.inst_id
#     institute_name = InstituteMaster.objects.all()
#     if request.user.is_superuser or request.user.role == 'admin':
#       institute_name = InstituteMaster.objects.filter(id=inst_id).first()
#     return render(request,'dashboard.html',{'institute_name':institute_name}) 

def institute_list(request):
    institutes = InstituteMaster.objects.all()
    return render(request, 'institute/institute-view.html', {'institutes': institutes})

def select_institute(request):
    # Check the user's role and filter institutes accordingly
    if request.user.is_superuser or request.user.role == 'admin':
        # Admin sees all institutes
        institutes = InstituteMaster.objects.all()
    else:
        # Other roles see only their allocated institute
        userinstitute = request.user.inst_id
        institutes = InstituteMaster.objects.filter(id=userinstitute)
    
        count = institutes.count()  # noqa: F841
    
    if request.method == 'POST':
        # Capture the selected institute ID from the form
        get_institute_id = request.POST.get('get_institute_id')
        print("ID received:", get_institute_id)
        selected_inst_id=InstituteMaster.objects.get(id=get_institute_id)
        # Update the user's inst_id with the selected institute
        request.user.inst_id = selected_inst_id
        request.user.save()

        # Redirect to the dashboard after selection
        return redirect('dashboard')
    
    # Render the template with the filtered institutes
    return render(request, 'institute/select-institute.html', {'institutes': institutes,'userinstitute': request.user.inst_id})


# def select_institute(request):
#     userinstitute = request.user.inst_id
#     institute = InstituteMaster.objects.filter(id=userinstitute)
#     # institute = InstituteMaster.objects.all()
#     count = institute.count()
#     selectinistitute = {'institute':institute,'count': count}
#     # if not request.user.role =='admin':
#     #     return HttpResponseForbidden("do not have permission ") 
#     if request.method == 'POST':        
#         get_institute_id =request.POST.get('get_institute_id')
#         print("id recieved:",get_institute_id)
#         request.user.inst_id = get_institute_id
#         request.user.save()

#         return redirect('dashboard')
#     return render(request,'institute/select-institute.html',{'institutes': institute,'userinstitute':userinstitute})

def institute_detail(request, pk):
    institute = get_object_or_404(InstituteMaster, pk=pk)
    print(institute.pk)  
    return render(request, 'institute/details-institute.html', {'institute': institute})


def institute_create(request):
    if request.method == 'POST':
        form = InstituteMasterForm(request.POST, request.FILES)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            institute = form.save()  # Save the form and get the saved institute instance
            send_mail(
                'Institute created successfully',
                'Your institute has been created successfully!',
                'your_email@example.com',  # Sender's email
                [institute.email],  # Institute's email from the saved instance
                fail_silently=False,
            )
            messages.success(request, 'Institute has been created successfully.')
            return redirect('institute_create')
    else:
        form = InstituteMasterForm()

    return render(request, 'institute/institute-form.html', {'form': form})

def institute_update(request, pk):
    institute = get_object_or_404(InstituteMaster, pk=pk)
    if request.method == 'POST':
        form = InstituteMasterForm(request.POST, request.FILES, instance=institute)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            updateinsitute=form.save()
            send_mail(
                'Your institute has been updated successfully!'
                'Your institute has been updated successfully!',
                'your_email@example.com',  # Sender's email
                [updateinsitute.email],  # Institute's email from the saved instance
                fail_silently=False,
            )
            messages.success(request, 'institute details have been updated successfully.')
            return redirect('institute_detail', pk=institute.pk)
    else:
        form = InstituteMasterForm(instance=institute)
    return render(request, 'institute/institute-edit.html', {'form': form})

def institute_toggle_status(request, pk):
    institute= get_object_or_404(InstituteMaster, pk=pk)
    # Toggle the status
    if institute.status == 'active':
        institute.status = 'inactive'
    else:
        institute.status = 'active'
    
    institute.save()
    messages.success(request, f'institute "{institute.name}" status updated to {institute.status}.')
    return redirect('institute_list')

