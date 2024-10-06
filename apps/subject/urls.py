from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.subject_dash,name='dashboard'), 
    path('', views.subject_list, name='subject_list'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subject/new/', views.subject_create, name='subject_create'),
    path('subject/<int:pk>/edit/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    path('fetch-years/', views.fetch_years, name='fetch_years'),
    path('fetch-semesters/', views.fetch_semesters, name='fetch_semesters'),


    path('fetch-subjects/', views.fetch_subjects, name='fetch_subjects'),
    path('syllabus/', views.syllabus_list, name='syllabus_list'),
    path('syllabus/<int:pk>/', views.syllabus_detail, name='syllabus_detail'),
    path('syllabus/new/', views.syllabus_create, name='syllabus_create'),
    path('syllabus/<int:pk>/edit/', views.syllabus_update, name='syllabus_update'),
    path('syllabus/<int:pk>/delete/', views.syllabus_delete, name='syllabus_delete'),
]
