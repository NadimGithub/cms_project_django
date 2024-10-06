from django import forms
from .models import TaskMaster

class TaskMasterForm(forms.ModelForm):
    class Meta:
        model = TaskMaster
        exclude = ['assigned_by','status']