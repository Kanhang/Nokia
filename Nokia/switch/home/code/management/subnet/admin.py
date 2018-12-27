
from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import subnet
# Register your models here.
class DataAdmin(admin.ModelAdmin):
    list_display = ('subnet', 'du', 'location', 'snmp_version', 'Community', 'Username', 'Password', 'Authority', 'Authentication_protocol', 'privacy_protocol', 'Passphase')
    list_per_page = 50
admin.site.register(subnet, DataAdmin)