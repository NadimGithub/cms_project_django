from django.db import models
from apps.course.models import CourseMaster
from apps.staff.models import StaffMaster
from apps.student.models import StudentMaster
from django.conf import settings  

class BookMaster(models.Model):
    id = models.AutoField(primary_key=True)
    book_images = models.ImageField(upload_to='book_profiles/')
    book_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(CourseMaster,on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    publish_date = models.DateField()
    copies_available = models.IntegerField()
    language = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    self_location = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    def __str__(self):
        return f'{self.author} - {self.isbn}'

class LibraryTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffMaster, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE, null=True, blank=True)
    book_id = models.ForeignKey(BookMaster, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    issued_to = models.CharField(max_length=10, choices=[('student', 'Student'), ('staff', 'Staff')])  # Updated field
    issued_by = models.CharField(max_length=30,null=True,blank=True)  # Updated field
    status = models.CharField(max_length=20,null=True,blank=True)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.book_id} issued to {self.issued_to}'
