from django.db import models
from apps.course.models import CourseMaster
from apps.subject.models import SubjectMaster
from apps.student.models import StudentMaster
from apps.staff.models import StaffMaster

# class ExamMaster(models.Model):
#     id = models.AutoField(primary_key=True)
    
#     course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
#     # year = models.CharField(max_length=50)
#     # semester = models.CharField(max_length=50)
#     # division = models.CharField(max_length=50)
#     sub_id = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     location = models.CharField(max_length=255)
#     duration = models.CharField(max_length=50)
#     type = models.CharField(max_length=20)
#     status = models.CharField(max_length=20)

class ExamPaper(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    subject = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffMaster, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    location  = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    questions = models.JSONField(default=list)  # JSON field to store multiple questions


    
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(ExamPaper, on_delete=models.CASCADE)
    std_id = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    year = models.CharField(max_length=50,null=True,blank=True)
    semester = models.CharField(max_length=50,null=True,blank=True)
    division = models.CharField(max_length=50,null=True,blank=True)
    subject = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE,null=True,blank=True)
    marks = models.IntegerField()
    total_marks = models.IntegerField(null=True,blank=True)
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,blank=True, null=True)


