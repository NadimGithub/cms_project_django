from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm 
from apps.staff.models import StaffMaster
from apps.student.models import StudentMaster
from django.contrib import messages

class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profilepage1.html'

    def get_context_data(self, **kwargs):
        profileview = super().get_context_data(**kwargs)
        user = self.request.user
        profileview.update({
            'user': user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'address': user.address,
            'mobile': user.mobile,
            'role': user.role,
            'profile_image': user.profile_image.url if user.profile_image else None,
        })
        return profileview
    
# @login_required
# def update_profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile')  # Redirect to a page that shows the updated profile
#     else:
#         form = ProfileForm(instance=user)

#     return render(request, 'update_profile.html', {'form': form})



@login_required
def update_profile(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_page')  # Redirect after successful update
        else:
            print(form.errors)  # Debugging: Print form errors if validation fails
    else:
        form = ProfileForm(instance=user)  # Populate form with existing user data

    return render(request, 'profilepage.html', {'form': form, 'user': user})