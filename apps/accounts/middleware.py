# myapp/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            # Define the allowed paths
            allowed_paths = [
                reverse('login'),
                reverse('register'),
                reverse('forgotpassword'),
            ]

            # Check if the path starts with any of the allowed paths or matches the change password pattern
            if not any(request.path.startswith(path) for path in allowed_paths) and not request.path.startswith('/changepassword/'):
                return redirect(settings.LOGIN_URL)
            
    #  def process_request(self, request):
    #     if not request.user.is_authenticated:
    #         if not request.path.startswith(reverse('login')) and not request.path.startswith(reverse('register')) and not request.path.startswith(reverse('forgotpassword')):
    #             return redirect(settings.LOGIN_URL)