from django.contrib import admin
from .models import StaffMaster, StaffAttendance, StaffLeave

@admin.register(StaffMaster)
class StaffMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'institute', 'status')
    search_fields = ('name', 'email')
    list_filter = ('status', 'institute')

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'date', 'status')
    search_fields = ('staff_id__name', 'status')
    list_filter = ('status', 'date')

@admin.register(StaffLeave)
class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'start', 'end', 'status', 'reason', 'verified_by', 'approved_by')
    search_fields = ('staff_id__name', 'status', 'reason')
    list_filter = ('status', 'start', 'end', 'verified_by', 'approved_by')
