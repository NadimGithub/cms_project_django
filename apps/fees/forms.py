from django import forms
from .models import FeesMaster, FeesStructure

class FeesMasterForm(forms.ModelForm):
    class Meta:
        model = FeesMaster
        exclude = ['remaining_amount','submitted_by']


class FeesStructureForm(forms.ModelForm):
    class Meta:
        model = FeesStructure
        exclude = ['status']

 