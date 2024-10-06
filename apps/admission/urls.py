from django.urls import path
from django.conf.urls.static import static
from cms_project import settings
from . import views

urlpatterns = [
    path('', views.admission_list, name='admission_list'),
    path('admission/<int:pk>/', views.admission_detail, name='admission_detail'),
    path('admission/new/', views.admission_create, name='admission_create'),
    path('admission/<int:pk>/edit/', views.admission_update, name='admission_update'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
