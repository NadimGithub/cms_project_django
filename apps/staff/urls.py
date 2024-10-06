from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Staff URLs
    #  path('dashboard', views.staff_dash,name='dashboard'),
    path('', views.staff_list, name='staff_list'),
    path('staff/<int:pk>/', views.staff_detail, name='staff_detail'),
    path('staff/', views.staff_create, name='staff_create'),
    path('staff/<int:pk>/edit/', views.staff_update, name='staff_update'),
    path('staff/<int:pk>/toggle_status/', views.toggle_staff_status, name='toggle_staff_status'),
     path('staff_report/', views.staff_report, name='staff_report'),


    path('staff_attendance_report',views.staff_attendance_report, name='staff_attendance_report'),
    path('staff_leave_report',views.staff_leave_report, name='staff_leave_report'),

    path('attendance/', views.staff_attendance_list, name='staff_attendance_list'),
    path('attendance/new/', views.staff_attendance, name='staff_attendance'),
    path('staff/update-attendance-status/<int:pk>/<str:status>/', views.update_attendance_status, name='update_attendance_status'),
    # Staff Leave URLs
    path('leave/', views.staff_leave_list, name='staff_leave_list'),
    path('leave/new/', views.staff_leave, name='staff_leave'),
    path('staff_leave_update/<int:pk>/edit/', views.staff_leave_update, name='staff_leave_update'),
   path('update-leave-status/<int:leave_id>/',views.update_leave_status, name='update_leave_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

