from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('dashboard', views.fees_dash,name='dashboard'), 
    path('', views.fees_structure_list, name='fees_structure_list'),
     path('fees_structure/toggle_status/<int:pk>/', views.toggle_fees_structure_status, name='fees_structure_toggle_status'),
    path('fees-structures/<int:pk>/', views.fees_structure_detail, name='fees_structure_detail'),
    path('fees-structures/create/', views.fees_structure_create, name='fees_structure_create'),
    path('fees-structures/<int:pk>/edit/', views.fees_structure_update, name='fees_structure_update'),
    path('fees_Structure/delete/<int:pk>/', views.fees_Structure_delete, name='fees_Structure_delete'),
    
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------
path('fetch-students/', views.fetch_students, name='fetch_students'),
path('export_to_excel/', views.export_to_excel_fees, name='export_to_excel_fees'),
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------

    path('fees', views.fees_list, name='fees_list'),
    path('fees/<int:pk>/', views.fees_detail, name='fees_detail'),
    path('fees/new/', views.fees_create, name='fees_create'),
    path('fees/<int:pk>/edit/', views.fees_update, name='fees_update'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
