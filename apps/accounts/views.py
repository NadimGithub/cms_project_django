# from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import CustomUser,Profile
from .helpers import send_forget_password_mail
from django.core.mail import send_mail
import uuid

def register(request):
    if request.method == 'POST':           
        form = CustomUserCreationForm(request.POST,request.FILES)
        print(form.data)
        if form.is_valid():
            print(form.errors)
           
            user = form.save()
            send_mail(
                'Registration Successful',
                f'Hi {user.first_name},\n\nThank you for registering at our site.http://127.0.0.1:8000/accounts/login/','',  # Use your email address
                [user.email],
                fail_silently=False,
            )
            print("hello")
            # login(request, user)
            django_login(request, user, backend='apps.accounts.backends.CustomBackend')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, "from user in login_view")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user, backend='apps.accounts.backends.CustomBackend')

            # Check user role to determine where to redirect
            if user.role == 'admin':
                return redirect('select_institute')
            else:
                return redirect('dashboard')
        else:
            # Add an error message and render the login page again
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')

    return render(request, 'login.html')




@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profilepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'address':user.address,
            'mobile': user.mobile,
            'role': user.role,
            'profile_image': user.profile_image.url if user.profile_image else None,
        })
        return context

def changepassword(request, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            try:
                # Retrieve the profile using the token
                profile_obj = Profile.objects.get(forget_password_token=token)
                user = profile_obj.user  # Access the CustomUser instance
                
                # Update the user's password
                user.set_password(new_password)
                user.save()
                
                # Clear the token after use
                profile_obj.forget_password_token = ''
                profile_obj.save()
                
                messages.success(request, 'Password has been reset successfully.')
                return redirect('login')
            except Profile.DoesNotExist:
                messages.error(request, 'Invalid or expired token.')
                return redirect('login')
    
        return render(request, 'changepassword.html')


def forgotpassword(request):
    print("forgot password page called")
    if request.method == 'POST':
        username= request.POST.get('username')
        print(username)
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=username)
            except CustomUser.DoesNotExist:
                messages.error(request, 'No user found with this username or email.')
                return render(request, 'forgotpassword.html')
        token = str(uuid.uuid4())
        profile, created = Profile.objects.get_or_create(user=user)
        profile.forget_password_token = token
        profile.save()

        # Send password reset email
        send_forget_password_mail(user.email, token)
        return render(request, 'login.html')

    return render(request,'forgotpassword.html')
