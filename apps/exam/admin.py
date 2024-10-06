from django.contrib import admin


from .models import ExamPaper,Result

# admin.site.register(ExamMaster)
admin.site.register(ExamPaper)
admin.site.register(Result)
