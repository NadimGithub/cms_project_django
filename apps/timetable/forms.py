from django import forms
from .models import TimetableMaster

class TimetableForm(forms.ModelForm):
    class Meta:
        model = TimetableMaster
        fields = '__all__'
        # widgets = {
        #     'start': forms.TimeInput(attrs={'type': 'time'}),
        #     'end': forms.TimeInput(attrs={'type': 'time'}),
        # }
