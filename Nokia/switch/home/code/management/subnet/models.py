# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class subnet(models.Model):
  snmp=(('v2c','v2c'),('v3','v3'))
  Auth=(('noAuthNoPriv','noAuthNoPriv'),('authNoPriv','authNoPriv'),('authPriv','authPriv'))
  AP=(('MD5','MD5'),('SHA','SHA'))
  PP=(('DES','DES'),('AES','AES'))
  subnet = models.CharField(max_length=100,  null=True)
  du = models.CharField(max_length=100, null=True, default="")
  location = models.CharField(max_length=100, null=True, default="")
  snmp_version = models.CharField(max_length=100, null=True,choices=snmp)
  Community = models.CharField(max_length=100, null=True,blank=True)
  Username = models.CharField(max_length=100, null=True, blank=True)
  Password = models.CharField(max_length=100, null=True, blank=True)
  Authority = models.CharField(max_length=100, null=True,choices=Auth, blank=True)
  Authentication_protocol = models.CharField(max_length=100, null=True, choices=AP, blank=True)
  privacy_protocol = models.CharField(max_length=100, null=True, choices=PP, blank=True)
  Passphase = models.CharField(max_length=100, null=True, default="", blank=True)
  # month=models.CharField(max_length=100,unique="True",null=True)
  # dell=models.CharField(max_length=100,default='0',null=True)
  # cisco = models.CharField(max_length=100,  default='0' ,null=True)
  # juniper = models.CharField(max_length=100, default='0',null=True )


  def __str__(self):
    #return u'%s %s %s %s %s %s %s %s %s %s' % (self.subnet )
    return u'%s' % (self.subnet )

