from django.contrib import admin

from .models import BookMaster,LibraryTransaction

admin.site.register(BookMaster)
admin.site.register(LibraryTransaction)
