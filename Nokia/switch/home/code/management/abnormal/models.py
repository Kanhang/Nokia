# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class abnormal(models.Model):

  date= models.CharField(max_length=100,  null=True)
  offline= models.CharField(max_length=100, null=True, default="")
  bkfailed=models.CharField(max_length=100, null=True, default="")
  nonstandard=models.CharField(max_length=100, null=True, default="")




  def __str__(self):


     return u'%s %s %s %s' % (self.date,self.bkfailed, self.offline,self.nonstandard)

