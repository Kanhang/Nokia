# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import food
# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = ('month','du','num')
    list_per_page = 50
admin.site.register(food, DataAdmin)