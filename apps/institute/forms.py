from django import forms
from .models import InstituteMaster
from django.core.exceptions import ValidationError

class InstituteMasterForm(forms.ModelForm):
    class Meta:
        model = InstituteMaster
        exclude = ['status']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        number = cleaned_data.get('number')
        email = cleaned_data.get('email')
        instance_id = self.instance.id  # Get the current instance ID

        # Check if the name already exists, excluding the current instance
        if InstituteMaster.objects.filter(name=name).exclude(id=instance_id).exists():
            self.add_error('name', 'Institute with this name already exists.')

        # Check if the number already exists, excluding the current instance
        if InstituteMaster.objects.filter(number=number).exclude(id=instance_id).exists():
            self.add_error('number', 'Institute with this phone number already exists.')

        # Check if the email already exists, excluding the current instance
        if InstituteMaster.objects.filter(email=email).exclude(id=instance_id).exists():
            self.add_error('email', 'Institute with this email already exists.')

        return cleaned_data