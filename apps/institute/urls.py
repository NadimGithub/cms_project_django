from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard', views.institute_dash,name='dashboard'),
    path('', views.institute_list, name='institute_list'),
    path('institute/<int:pk>/', views.institute_detail, name='institute_detail'),
    path('institute/', views.institute_create, name='institute_create'),
    path('institute/<int:pk>/edit/', views.institute_update, name='institute_update'),
    path('select_institute/', views.select_institute,name='select_institute'),
    path('institute/toggle-status/<int:pk>/',views.institute_toggle_status, name='institute_toggle_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

