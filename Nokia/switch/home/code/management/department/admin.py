# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import department
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('Tribe_name', 'Tribe', 'Squad_groups','Squad','LabOps','LabOrder','LabSupport')
    change_list_template = "department_change_list.html"
admin.site.register(department,DepartmentAdmin)
