from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.course_dash,name='dashboard'),
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/', views.course_create, name='course_create'),
    path('course/<int:pk>/edit/', views.course_update, name='course_update'),
    path('course/toggle-status/<int:pk>/',views.course_toggle_status, name='course_toggle_status'),

    path('add/', views.add_division, name='add_division'),
    path('division_view/', views.view_division, name='view_division'),
    path('division/<int:pk>/update/',views.division_update, name='division_update'),
]
 