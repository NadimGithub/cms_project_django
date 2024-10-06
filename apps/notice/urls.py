from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.notice_dash,name='notice_dash'), 
    path('', views.notice_list, name='notice_list'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notice/new/', views.notice_create, name='notice_create'),
    path('notice/<int:pk>/edit/', views.notice_update, name='notice_update'),
    path('notice/delete/<int:pk>/', views.notice_delete, name='notice_delete'),
]
 