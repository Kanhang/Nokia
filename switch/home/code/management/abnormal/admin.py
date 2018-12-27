
from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import abnormal
# Register your models here.
class AbnormalAdmin(admin.ModelAdmin):
    list_display = ('date', 'offline', 'bkfailed','nonstandard',)
    list_per_page = 50
admin.site.register(abnormal, AbnormalAdmin)