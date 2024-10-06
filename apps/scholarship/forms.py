# forms.py
from django import forms
from .models import ScholarshipMaster

class ScholarshipForm(forms.ModelForm):
    # school_documents = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #     required=False
    # )

    class Meta:
        model = ScholarshipMaster
        fields ='__all__'#['student_id', 'school_documents', 'status']
 