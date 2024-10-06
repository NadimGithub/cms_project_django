from django.conf import settings
from django.db import models
from apps.institute.models import InstituteMaster
from django.utils import timezone

class NoticeMaster(models.Model):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('inactive', 'inactive'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_of_publish = models.DateField()
    date_of_end = models.DateField()
    status = models.CharField(max_length=20,default='active')
    notice_type = models.CharField(max_length=50)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL
  