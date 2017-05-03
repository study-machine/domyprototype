from django.contrib import admin

# Register your models here.

from .models import *


class PrototypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Prototype, PrototypeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)


class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'active', 'order', 'update_time', 'create_time']
    list_editable = ['active', 'order']


admin.site.register(Carousel, CarouselAdmin)
