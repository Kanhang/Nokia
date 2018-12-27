
from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import brand
# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = ('month', 'type', 'num')
    list_per_page = 50
admin.site.register(brand, DataAdmin)