from django.contrib import admin

from .models import StudentMaster,StudentDetails,StudentAttendance,StudentLeave,StudentProgress,TempAddress,PermAddress,Document

admin.site.register(StudentMaster)
admin.site.register(StudentDetails)
admin.site.register(StudentAttendance)
admin.site.register(StudentLeave)
admin.site.register(StudentProgress)
admin.site.register(TempAddress)
admin.site.register(PermAddress)
admin.site.register(Document)

