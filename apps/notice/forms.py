from django import forms
from .models import NoticeMaster

class NoticeMasterForm(forms.ModelForm):
    class Meta:
        model = NoticeMaster
        exclude = ['status','submitted_by']
  