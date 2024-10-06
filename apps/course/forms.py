from django import forms
from .models import CourseMaster,DivisionMaster
from django.core.exceptions import ValidationError
# import re


class CourseMasterForm(forms.ModelForm):
    class Meta:
        model = CourseMaster
        # fields = '__all__'
        exclude=['id','institute_id','status','submitted_by']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Name field cannot be empty.')
        # You can add more validations as needed
        return name

    def clean_intake_capacity(self):
        intake_capacity = self.cleaned_data.get('intake_capacity')
        if intake_capacity is None or intake_capacity <= 5:
            raise ValidationError('Intake capacity must be greater than five.')
        return intake_capacity
    
class DivisionMasterForm(forms.ModelForm):
    class Meta:
        model = DivisionMaster
        # fields = '__all__'
        exclude=['status','submitted_by']