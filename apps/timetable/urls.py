from django.urls import path
from . import views

urlpatterns = [ 
    # path('dashboard', views.timetable_dash,name='dashboard'), 
    path('', views.timetable_list, name='timetable_list'),
    path('create/', views.timetable_create, name='timetable_create'),
    path('<int:pk>/update/', views.timetable_update, name='timetable_update'),
    path('<int:pk>/detail', views.timetable_detail, name='timetable_detail'),
    path('<int:pk>/delete/', views.timetable_delete, name='timetable_delete'),
]
