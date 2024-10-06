from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.subject.models import SubjectMaster
from apps.institute.models import InstituteMaster
from apps.staff.models import StaffMaster
from apps.accounts.models import CustomUser
from apps.course.models import CourseMaster



class StudentMaster(models.Model):
    id = models.AutoField(primary_key=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_image = models.ImageField(upload_to='student_profiles/')
    user = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.PROTECT)
   
    institute = models.ForeignKey(InstituteMaster, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, default='student')

    def __str__(self):
        return f"{self.id}"

class StudentDetails(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'general'),
        ('obc', 'obc'),
        ('sc', 'sc'),
        ('st', 'st'),
    ]
    NATIONALITY_CHOICES = [
        ('indian', 'Indian'),
        ('other', 'Other')
    ]
    ADMISSION_CHOICES = [
        ('cap', 'CAP'),
        ('management', 'Management')
    ]
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,null=True,blank=True)
    year = models.CharField(max_length=50,null=True,blank=True)  # Make sure these fields are correct
    semester = models.CharField(max_length=50,null=True,blank=True)
    division = models.CharField(max_length=50,null=True,blank=True)
    student = models.OneToOneField(StudentMaster, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    blood_group = models.CharField(max_length=10)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    caste = models.CharField(max_length=50)
    education_qualification = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=10, choices=NATIONALITY_CHOICES)
    admission_type = models.CharField(max_length=10, choices=ADMISSION_CHOICES)
    cap_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.registration_number



class StudentAttendance(models.Model):

    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE,null=True,blank=True)
    year = models.CharField(max_length=50,null=True,blank=True)
    semester = models.CharField(max_length=50,null=True,blank=True)
    division = models.CharField(max_length=50,null=True,blank=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectMaster, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffMaster, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.subject.name} - {self.date}"


class StudentLeave(models.Model):
    status_choices= (
        ('pending', 'pending'),
        ('Approved', 'Approved'),
        ('rejected', 'rejected'),  
    )
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=10,choices=status_choices ,default='pending')
    reason = models.TextField()
    student_approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='student_approved_leaves')
    def __str__(self):
        return f"{self.student} - {self.start} to {self.end}"

class StudentProgress(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=10)  # Assuming it's a CharField, adjust as needed
    marks = models.FloatField()
    grade = models.CharField(max_length=2)
    attendance = models.FloatField()  # Or another suitable type for your progress bar
    def __str__(self):
        return f"{self.student} - {self.course_id}"
    
class TempAddress(models.Model):
    tempaddress_id= models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE,null=True ,blank=True)
    temp_state = models.CharField(max_length=50)
    temp_district = models.CharField(max_length=50)
    temp_taluka = models.CharField(max_length=50)
    temp_city = models.CharField(max_length=50)
    temp_pincode = models.CharField(max_length=6)
    temp_address = models.CharField(max_length=50)

class PermAddress(models.Model):
    permaddress_id= models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE,null=True ,blank=True)
    perm_state = models.CharField(max_length=50)
    perm_district = models.CharField(max_length=50)
    perm_taluka = models.CharField(max_length=50)
    perm_city = models.CharField(max_length=50)
    perm_pincode = models.CharField(max_length=6)
    perm_address = models.CharField(max_length= 50)

class Document(models.Model):
    document_id= models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.ForeignKey(StaffMaster, on_delete=models.CASCADE,null=True ,blank=True)
    document_name = models.CharField(max_length=50)
    document = models.FileField()
    document_uploded= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True ,blank=True)