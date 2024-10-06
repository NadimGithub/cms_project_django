from django import forms
from .models import AdmissionMaster
from django.utils import timezone
from django.core.exceptions import ValidationError

class AdmissionMasterForm(forms.ModelForm):
    class Meta:
        model = AdmissionMaster
        exclude = ['admission_by']
def clean(self):
        # Ensure the date_of_apply is not in the future
        if self.date_of_apply > timezone.now().date():
            raise ValidationError('The application date cannot be in the future.')