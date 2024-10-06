from django.db import models
from django.contrib.auth.models import User 
from apps.institute.models import InstituteMaster
from apps.course.models import CourseMaster
from django.conf import settings 
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models





class StaffMaster(models.Model):
    Role_choices= (
        ('principal', 'Principal'),
        ('vice_principal', 'Vice_Principal'),
        ('hod', 'Hod'),
        ('teacher', 'Teacher'),
        ('accountant', 'Accountant'),
        ('clark', 'Clark'),
        ('examinetor', 'Examinetor'),
        ('librarian', 'Librarian'),
        ('lab_assistant', 'Lab_Assistant'),
        
    )
    status=(
        ('active', 'Active'),
        ('inactive', 'Inactive'), 
    )
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,null=True,blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    number = models.CharField(max_length=15)
    do_join =  models.DateField(null=True, blank=True)
    do_leaving =  models.DateField(null=True, blank=True)
    email = models.TextField(unique=True)
    status = models.CharField(max_length=20, default='active')
    dob = models.DateField()
    profile = models.ImageField(upload_to='profiles/')
    blood_group = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    user = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.PROTECT)
    institute = models.ForeignKey(InstituteMaster, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=Role_choices)
    


class StaffAttendance(models.Model):
    status_choices = (('Present', 'Present'), ('Absent', 'Absent'))
    
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=timezone.now, editable=False)
    status = models.CharField(max_length=10, choices=status_choices, default='Absent')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL

    def __str__(self):
        return f"{self.staff_id} - {self.date} - {self.status}"

class StaffLeave(models.Model):
    status_choices= (
        ('pending', 'pending'),
        ('Approved', 'Approved'),
        ('rejected', 'rejected'),  
    )
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=10,choices=status_choices ,default='pending')
    reason = models.TextField()
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='verified_leaves', on_delete=models.SET_NULL, null=True, blank=True
    )  # Updated field
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='approved_leaves', on_delete=models.SET_NULL, null=True,blank=True    )  # Updated field

