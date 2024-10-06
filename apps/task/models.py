from django.db import models
from apps.accounts.models import CustomUser 
from apps.staff.models import StaffMaster  # Import settings to reference AUTH_USER_MODEL

class TaskMaster(models.Model):
    id = models.AutoField(primary_key=True)
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    task = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    description = models.TextField(blank=True)
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Assigned by a user
    assigned_to = models.ForeignKey(StaffMaster, on_delete=models.SET_NULL, null=True, blank=True)  # Assigned to staff member
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateField()

    def __str__(self):
        return self.task
    
