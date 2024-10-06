from django.urls import path
from . import views

urlpatterns = [
    # path('dashboard', views.scholarship_dash,name='dashboard'), 
    path('', views.scholarship_list, name='scholarship_list'),
    path('create/', views.scholarship_create, name='scholarship_create'),
    path('<int:pk>/update/', views.scholarship_update, name='scholarship_update'),
    path('<int:pk>/delete/', views.scholarship_delete, name='scholarship_delete'),
]
