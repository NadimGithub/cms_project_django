from django.db import models
from apps.institute.models import InstituteMaster
from django.conf import settings 

class CourseMaster(models.Model):
    id = models.AutoField(primary_key=True)
    status_choices= (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),  
    )

    name = models.CharField(max_length=255)
    institute_id = models.ForeignKey(InstituteMaster, on_delete=models.CASCADE)
    start_date = models.DateField()
    status = models.CharField(max_length=20, default='active')
    intake_capacity = models.IntegerField()
    durstion = models.CharField(max_length=20, null=True, blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL

    def __str__(self):
        return self.name
    
class DivisionMaster(models.Model):
    id = models.AutoField(primary_key=True)
    status_choices= (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),  
    )
    semester_choices= (
        ('1 semester', '1 semester'),
        ('2 semester', '2 semester'),
        ('3 semester', '3 semester'),
        ('4 semester', '4 semester'),
        ('5 semester', '5 semester'),
        ('6 semester', '6 semester'),
        ('7 semester', '7 semester'),
        ('8 semester', '8 semester'),  
    )
    year_choices= (
        ('1st year', '1st year'),
        ('2nd year', '2nd year'),
        ('Direct second year', 'Direct second year'),
        ('3rd year', '3rd year'),
        ('4th year', '4th year'),
    )
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=20,choices=year_choices)
    semester = models.CharField(max_length=20,choices=semester_choices)
    status = models.CharField(max_length=20, default='active')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL

    def __str__(self):
        return self.name