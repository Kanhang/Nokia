# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import device

from django.utils.safestring import mark_safe
# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields=('Status','Update_time')
    list_display = ('IPAddress', 'Device_type','Tribe_name', 'contact_detail','Location','Status','Update_time')

    change_list_template = "device_change_list.html"
    def  contact_detail(self,obj):
        Tribe_name=obj.Tribe_name
        id=obj.id
        return mark_safe('<a href="http://10.110.23.254/admin/department/department/{id}/change/">show</a>'.format(id=id))

admin.site.register(device,DeviceAdmin)
#http://10.110.23.254/admin/department/department/4/change/