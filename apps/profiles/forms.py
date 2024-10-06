from django import forms
# Update this to the correct import
from apps.accounts.models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile','profile_image']  # Include fields you want to update

