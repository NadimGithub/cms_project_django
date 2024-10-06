from django import forms
from .models import StudentMaster, StudentDetails, StudentAttendance, StudentLeave, StudentProgress, TempAddress, PermAddress, Document

class StudentMasterForm(forms.ModelForm):
    class Meta:
        model = StudentMaster
        exclude = ['status', 'role', 'institute']
        widgets = {
            'dob': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date input
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder text
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        email = cleaned_data.get('email')
        instance_id = self.instance.id

        # Check if the number already exists, excluding the current instance
        if StudentMaster.objects.filter(number=number).exclude(id=instance_id).exists():
            self.add_error('number', 'A student with this phone number already exists.')

        # Check if the email already exists, excluding the current instance
        if StudentMaster.objects.filter(email=email).exclude(id=instance_id).exists():
            self.add_error('email', 'A student with this email already exists.')

        return cleaned_data

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        exclude = ['state', 'district', 'course_name']

    def clean(self):
        cleaned_data = super().clean()
        registration_number = cleaned_data.get('registration_number')
        instance_id = self.instance.id

        # Check if the registration number already exists, excluding the current instance
        if StudentDetails.objects.filter(registration_number=registration_number).exclude(id=instance_id).exists():
            self.add_error('registration_number', 'A student with this registration number already exists.')

        return cleaned_data

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        exclude = ['date']

class StudentLeaveForm(forms.ModelForm):
    class Meta:
        model = StudentLeave
        fields = ['reason', 'start', 'end']

class StudentProgressForm(forms.ModelForm):
    class Meta:
        model = StudentProgress
        fields = '__all__'

class tempaddressForm(forms.ModelForm):
    class Meta:
        model = TempAddress
        fields = '__all__'

class permaddressForm(forms.ModelForm):
    class Meta:
        model = PermAddress
        fields = '__all__'

class documentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
