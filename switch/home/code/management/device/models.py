# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection
from django.db import models
from django.utils.functional import lazy
from department.models import department

# Create your models here.
def retdu():
 try:
     choices=[(str(o),str(o))for o in department.objects.all()]

     return choices
 except Exception,e:
     print e.message
     return((None,None),)

class device(models.Model):
    type = (('Switch', 'Switch'), ('Server', 'Server'), ('PB', 'PB'),)
    IPAddress = models.CharField(max_length=100, null=True)
    Location = models.CharField(max_length=100, default='', null=True)
    Device_type = models.CharField(max_length=100, null=True,choices=type, blank=True)
    Status = models.BooleanField(default=False)
    Update_time = models.CharField(max_length=100, default='', blank=True)
    Tribe_name = models.CharField(max_length=100, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(device, self).__init__(*args, **kwargs)
        self._meta.get_field('Tribe_name').choices = lazy(retdu, tuple)()

    def __str__(self):
        return u'%s' % (self.IPAddress)

