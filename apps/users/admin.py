from django.contrib import admin

# Register your models here.
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nick_name', 'last_login']


admin.site.register(UserProfile, UserProfileAdmin)
