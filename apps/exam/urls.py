from django.urls import path
from . import views

urlpatterns = [

path('dashboard', views.exam_dash,name='dashboard'), 

    # path('', views.exam_list, name='exam_list'),
    # path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    # path('exam/new/', views.exam_create, name='exam_create'),
    # path('exam/<int:pk>/edit/', views.exam_update, name='exam_update'),
    
    path('exam-papers/', views.exam_paper_list, name='exam_paper_list'),
    path('exam-papers/edit/<int:exam_paper_id>/', views.edit_exam_paper, name='edit_exam_paper'),
    path('exam-papers/create/', views.exam_paper_create, name='exam_paper_create'),
    path('exam-paper/<int:pk>/',views.exam_paper_view, name='exam_paper_view'),
    path('exam-paper/',views.exam_paper_view, name='exam_paper_view'),
    # path('exam_paper/edit/<int:exam_paper_id>/', views.edit_exam_paper, name='edit_exam_paper'),
    path('update_exam_status/<int:exam_id>/', views.update_exam_status, name='update_exam_status'),
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------
    path('fetch-years/', views.fetch_years, name='fetch_years'),
    path('fetch-semesters/', views.fetch_semesters, name='fetch_semesters'),
    path('fetch-divisions/', views.fetch_divisions, name='fetch_divisions'),
    path('fetch_students_result/', views.fetch_students_result, name='fetch_students_result'),
    path('fetch_exams/', views.fetch_exams, name='fetch_exams'),
    
    
    # path('exam/attendance/fetch_exam/', views.fetch_exam, name='fetch_exam'),
#---------------------This is for Ajax call---------------------------------------------------------------------------------------------------------------
        
    path('results/', views.result_list, name='result_list'),
    path('results/<int:pk>/', views.result_detail, name='result_detail'),
    path('results/create/', views.result_create, name='result_create'),
    path('results/<int:pk>/edit/', views.result_update, name='result_update'),
]