from django.conf import settings
from django.db import models
from apps.student.models import StudentMaster
from apps.course.models import CourseMaster

class FeesStructure(models.Model):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('inactive', 'inactive'),
    ]
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    cast = models.CharField(max_length=50)
    is_scholarship = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.CharField(max_length=10)
    status = models.CharField(max_length=20,default='active')
    name = models.CharField(max_length=100)
    is_gap = models.CharField(max_length=20)

class FeesMaster(models.Model): 
    id = models.AutoField(primary_key=True)
    course= models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fees_structure = models.ForeignKey(FeesStructure, on_delete=models.CASCADE)
    fees_type = models.CharField(max_length=50)
    date = models.DateField()
    status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    upload_document = models.ImageField(upload_to='fees_documents/', null=True, blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL