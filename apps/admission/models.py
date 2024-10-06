from django.db import models
from apps.student.models import StudentMaster
from apps.course.models import CourseMaster
from apps.fees.models import FeesStructure
from apps.accounts.models import CustomUser


class AdmissionMaster(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    course_id = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    admission_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True) # Updated field
    fees_structure = models.ForeignKey(FeesStructure, on_delete=models.CASCADE)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2)
    fees_unpaid = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_apply = models.DateField()
   

    def __str__(self):
        return f'{self.id} {self.student_id} - {self.course_id} '
