from django import forms
from .models import StaffMaster, StaffAttendance, StaffLeave

class StaffMasterForm(forms.ModelForm):
    class Meta:
        model = StaffMaster
        exclude=['status','institute','do_leaving']
        
    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        email = cleaned_data.get('email')
        instance_id = self.instance.id 


        # Check if the number already exists, excluding the current instance
        if StaffMaster.objects.filter(number=number).exclude(id=instance_id).exists():
            self.add_error('number', 'staff with this phone number already exists.')

        # Check if the email already exists, excluding the current instance
        if StaffMaster.objects.filter(email=email).exclude(id=instance_id).exists():
            self.add_error('email', 'staff with this email already exists.')

        return cleaned_data

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendance
        exclude=['submitted_by']
        

class StaffLeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        exclude=['staff_id','status']
       


   