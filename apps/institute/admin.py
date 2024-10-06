from django.contrib import admin
from .models import InstituteMaster

@admin.register(InstituteMaster)
class InstituteMasterAdmin(admin.ModelAdmin):
    list_display = ('id',)


