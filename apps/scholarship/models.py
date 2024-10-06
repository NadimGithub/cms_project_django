from django.db import models
# from apps.staff.models import Staff_Master  
# from apps.institute.models import Institute_master  
class Document(models.Model):
    file = models.FileField(upload_to='school_documents/')

    
class ScholarshipMaster(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=255)
    school_documents = models.ManyToManyField(Document, blank=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Scholarship for student {self.student_id}"
 