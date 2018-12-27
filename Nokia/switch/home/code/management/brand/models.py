# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class brand(models.Model):

  month = models.CharField(max_length=100,  null=True)
  type = models.CharField(max_length=100, null=True, default="")
  num = models.CharField(max_length=100, null=True, default="")
  # month=models.CharField(max_length=100,unique="True",null=True)
  # dell=models.CharField(max_length=100,default='0',null=True)
  # cisco = models.CharField(max_length=100,  default='0' ,null=True)
  # juniper = models.CharField(max_length=100, default='0',null=True )


  def __str__(self):
    #return u'%s %s %s %s %s %s %s %s %s %s' % (self.month,self.dell,  self.cisco, self.juniper, )
    return u'%s %s %s' % (self.month,self.type,  self.num, )

