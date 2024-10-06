from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>/', views.task_update, name='task_update'),
    path('update_task_status/<int:leave_id>/', views.update_task_status, name='update_task_status'),
]
