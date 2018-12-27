# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import page
# Register your models here.


class pageAdmin(admin.ModelAdmin):
    list_display = ['page_index_count','refresh_count']


admin.site.register(page,pageAdmin)