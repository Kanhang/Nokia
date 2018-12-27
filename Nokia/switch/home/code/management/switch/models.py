# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.html import format_html
from django.contrib import admin
# Create yr models here.

'''
def set_path(instance, filename):
    path = "/root/backup/"+instance.Location+"/"+instance.DU+"/"+instance.Type+"/"+instance.IPAddress + "/"

    return path


'''


class BackUp(models.Model):
  snmp=(('v2c','v2c'),('v3','v3'))
  Auth=(('noAuthNoPriv','noAuthNoPriv'),('authNoPriv','authNoPriv'),('authPriv','authPriv'))
  AP=(('MD5','MD5'),('SHA','SHA'))
  PP=(('DES','DES'),('AES','AES'))

  IPAddress=models.CharField(max_length=100, unique=True,null=True)
  Type=models.CharField(max_length=100,blank= True, null=True,)
  Model = models.CharField(max_length=100, blank=True, null=True, )
  Version = models.CharField(max_length=100, blank=True, null=True, )
  DU=models.CharField(max_length=100,null=True,)
  Name = models.CharField(max_length=100,  null=True,blank=True)
  Location = models.CharField(max_length=100, null=True)
  BackupFailed = models.CharField(max_length=100,blank= True, null=True,)
  Last_backup_date= models.CharField(max_length=100,blank= True, null=True)
  Online=models.BooleanField(default=False)
  Stdname=models.BooleanField(default=False)
  Runtime = models.CharField(max_length=100, blank=True, null=True)
  snmp_version = models.CharField(max_length=100, null=True,blank=True,choices=snmp)
  Community = models.CharField(max_length=100, null=True,blank=True)
  Username = models.CharField(max_length=100, null=True, blank=True)
  Password = models.CharField(max_length=100, null=True, blank=True)
  Authority = models.CharField(max_length=100, null=True,choices=Auth, blank=True)
  Authentication_protocol = models.CharField(max_length=100, null=True, choices=AP, blank=True)
  privacy_protocol = models.CharField(max_length=100, null=True, choices=PP, blank=True)
  Passphase = models.CharField(max_length=100, null=True, default="", blank=True)
  Snmpv3 = models.CharField(max_length=100,blank= True, null=True)
  Note=models.CharField(max_length=1000,blank=True,null=True)

  def colored_Snmpv3(self):
      if self.Snmpv3 == 'ON':
          color_code = 'green'
      else:
          color_code = '#dd4747'
      return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.Snmpv3,
        )
        
  colored_Snmpv3.short_description = u"Snmpv3"


  def __str__(self):
    return u'%s' % (self.IPAddress)
    
  def toJSON(self):
    import json
    return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
  

  class Meta:
     verbose_name = u"switches' info"
     verbose_name_plural = verbose_name
