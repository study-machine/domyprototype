from django.contrib import admin

# Register your models here.

from .models import *


class VersionAdmin(admin.ModelAdmin):
    list_display = ['version_number', 'desc', 'version_update_time']
    list_editable = ['version_number', 'version_update_time']


admin.site.register(Version, VersionAdmin)
