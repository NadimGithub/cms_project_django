from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'address', 'role','profile_image']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # if 'profile_image' in self.files:
            #     user.profile_image = self.files['profile_image']
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username/Email/Mobile')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise ValidationError("Username and password are required.")

        user = None

        for field in ['username','email','mobile']:
            try:
                user = CustomUser.objects.get(**{field: username})
                break
            except CustomUser.DoesNotExist:
                continue

        if user is None:
            raise ValidationError("User with this username/email/mobile does not exist.")

        if not user.check_password(password):
            raise ValidationError("Password is incorrect.")

        self.user_cache = user
        return cleaned_data
    
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'mobile', 'address', 'role', 'profile_image']
#         widgets = {
#             'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields['profile_image'].required = False  # Make profile image optional

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile', 'role', 'profile_image']
        # widgets = {
        #     'profile_image': forms.ClearableFileInput(attrs={'multiple': True}),
        # }