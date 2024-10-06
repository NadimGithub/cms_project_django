from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import TaskMaster
from apps.staff.models import StaffMaster
from .forms import TaskMasterForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q


def task_list(request):
    task_list = TaskMaster.objects.all()

    # Get the start and end dates from GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    query = request.GET.get('q')

    # Filter by date range if both start and end dates are provided
    if start_date and end_date:
        task_list = task_list.filter(deadline__range=[start_date, end_date])

    # Search by task name, description, assigned by, assigned to, or status
    if query:
        task_list = task_list.filter(
            Q(task__icontains=query) |
            Q(description__icontains=query) |
            Q(assigned_by__username__icontains=query) |  # Adjust if your CustomUser model has a different field
            Q(assigned_to__name__icontains=query) |
            Q(status__icontains=query)  # Search by status
        )

    paginator = Paginator(task_list, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    return render(request, 'task/task_list.html', {
        'task': tasks,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
    })

def task_detail(request, pk):
    task = get_object_or_404(TaskMaster, pk=pk)
    return render(request, 'task/task_detail.html', {'task': task})



def task_create(request):
    staffs = StaffMaster.objects.all()
    if request.method == 'POST':
        form = TaskMasterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()

            # Sending an email to the assigned staff
            assigned_staff = task.assigned_to  # Assuming assigned_to field is in the TaskMaster model
            assigned_by = task.assigned_by  # This is the user who assigned the task
            
            send_mail(
                        subject='New Task Assigned',
                        message=(
                            f'Dear {assigned_staff.name},\n\n'
                            f'You have been assigned a new task titled "{task.task}" by {assigned_by.username}.\n\n'  # Use appropriate attribute like username or name
                            f'Please check your dashboard for more details.\n\n'
                            f'Thank you.'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[assigned_staff.email],
                        fail_silently=False,
                    )

            return redirect('task_list')
    else:
        form = TaskMasterForm()
    return render(request, 'task/task.html', {'form': form, 'staff': staffs})

def update_task_status(request, leave_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        task = get_object_or_404(TaskMaster, id=leave_id)
        if status in dict(TaskMaster.STATUS_CHOICES).keys():  # Make sure status is valid
            task.status = status
            if status in ['completed', 'in progress']:
                task.approved_by = request.user  # Assuming this is needed in your logic
            task.save()  # Save task changes
            messages.success(request, 'Task status updated successfully!')
        else:
            messages.error(request, 'Invalid status!')
    return redirect('task_list')  # Redirect to the appropriate view

def task_update(request, pk):
    staffs = StaffMaster.objects.all()
    task = get_object_or_404(TaskMaster, pk=pk)  # This line raises the error
    if request.method == 'POST':
        form = TaskMasterForm(request.POST,instance=task)
        print(form.data)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskMasterForm(instance=task)
    return render(request, 'task/task-edit.html', {'forms': form ,'staffs':staffs})

# def task_update(request, pk):
#     task = get_object_or_404(TaskMaster, pk=pk)
#     if request.method == 'POST':
#         form = TaskMasterForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('task_detail', pk=task.pk)
#     else:
#         form = TaskMasterForm(instance=task)
#     return render(request, 'task/task-edit.html', {'form': form})
