from django.conf import settings
from django.db import models
from apps.course.models import CourseMaster

class SubjectMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[('theory', 'Theory'), ('practical', 'Practical'),('both', 'Both')])
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,null=True,blank=True)
    marks_credits = models.IntegerField()
    duration = models.CharField(max_length=50)
    pattern = models.CharField(max_length=50)
    year = models.CharField(max_length=50,null=True,blank=True)
    semester = models.CharField(max_length=50,null=True,blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL

class SyllabusMaster(models.Model):
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,null=True,blank=True)
    syllabus_id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
    unit = models.CharField(max_length=255)
    points_sub_points = models.TextField()
    year = models.CharField(max_length=50,null=True,blank=True)
    duration = models.CharField(max_length=50)
    marks = models.IntegerField()
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Use AUTH_USER_MODEL

