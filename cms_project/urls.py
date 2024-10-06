
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView   
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('authentication/', include('apps.authentication.urls')),
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('profile/', include('apps.profiles.urls')),
    path('courses/', include('apps.course.urls')),
    path('subjects/', include('apps.subject.urls')),
    path('admissions/', include('apps.admission.urls')),
    path('students/', include('apps.student.urls')),
    path('exams/', include('apps.exam.urls')),
    path('tasks/', include('apps.task.urls')),
    path('notices/', include('apps.notice.urls')),
    path('fees/', include('apps.fees.urls')),
    path('library/', include('apps.library.urls')),
    path('institutes/', include('apps.institute.urls')),
    path('staff/', include('apps.staff.urls')),
    path('timetables/', include('apps.timetable.urls')),
    path('scholarships/', include('apps.scholarship.urls')),

    #  path('institute/', TemplateView.as_view(template_name='institute/institute_form.html'),name = 'institute'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)