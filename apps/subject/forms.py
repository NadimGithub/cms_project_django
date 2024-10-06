from django import forms
from .models import SubjectMaster, SyllabusMaster

class SubjectMasterForm(forms.ModelForm):
    class Meta:
        model = SubjectMaster
        # fields = '__all__'
        exclude =['id','submitted_by']

class SyllabusMasterForm(forms.ModelForm):
    class Meta:
        model = SyllabusMaster
        exclude =['submitted_by']
