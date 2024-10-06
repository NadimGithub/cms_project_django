from django.urls import path
from . import views
from .views import ProfilePageView ,update_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', ProfilePageView.as_view(), name='profile_page'),
    path('update-profile/', update_profile, name='update_profile'), # Add this line
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
