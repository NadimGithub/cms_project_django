from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.student_dash,name='dashboard'), 
    path('', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/', views.student_detail, name='student_detail'),

    path('student/create/', views.student_create, name='student_create'),
    path('student/update/<int:pk>/', views.student_update, name='student_update'),
    path('student/toggle-status/<int:pk>/',views.student_toggle_status, name='student_toggle_status'),
 
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------
    path('etch_students_attendance/', views.fetch_students_attendance, name='fetch_students_attendance'),
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------

    # Student Details
    # path('save-address/', views.save_address, name='save_address'),
    path('student/details/', views.student_details_create, name='student_details_create'),
    # path('student/details/<int:registration_number>/edit/', views.student_details_update, name='student_details_update'),
    # path('student/details/<int:registration_number>/delete/', views.student_details_delete, name='student_details_delete'),
    
    # Attendance
    path('attendance/', views.student_attendance_list, name='student_attendance_list'),
    path('attendance/create/', views.student_attendance_create, name='student_attendance_create'),
    path('attendance/<int:pk>/edit/', views.student_attendance_update, name='student_attendance_update'),
    path('attendance/<int:pk>/delete/', views.student_attendance_delete, name='student_attendance_delete'),
        path('students/attendance/<int:pk>/toggle-status/', views.attandance_toggle_status, name='attandance_toggle_status'),

    # Leave
    path('leave/', views.student_leave_list, name='student_leave_list'),
    path('leave/create/', views.student_leave_create, name='student_leave_create'),
    path('leave/<int:pk>/edit/', views.student_leave_update, name='student_leave_update'),
    path('student_update_leave_status/<int:leave_id>/',views.student_update_leave_status, name='student_update_leave_status'),
    # Progress
    path('progress/', views.student_progress_list, name='student_progress_list'),
    path('progress/create/', views.student_progress_create, name='student_progress_create'),
    path('progress/<int:pk>/edit/', views.student_progress_update, name='student_progress_update'),
    path('progress/<int:pk>/delete/', views.student_progress_delete, name='student_progress_delete'),

    path('tempaddress/', views.student_tempaddress, name='student_tempaddress'),
    path('permaddress/', views.student_permaddress, name='student_permaddress'),
    path('documents/', views.Documents, name='documents'),
    path('students/update-document/<int:student_id>/', views.update_document, name='update_document'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),  # URL for deleting the document
]
