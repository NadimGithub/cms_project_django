from django.db import models
from apps.staff.models import StaffMaster 
from apps.course.models import CourseMaster
from apps.subject.models import SubjectMaster  
# from institute.models import Institute_master  # Adjust import based on actual location

class TimetableMaster(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start = models.TimeField()
    end = models.TimeField()
    subject_id = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE)
