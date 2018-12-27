# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class food(models.Model):
  month = models.CharField(max_length=100,  null=True)
  du= models.CharField(max_length=100,default='',null=True)
  num= models.CharField(max_length=100, default='0', null=True)

  # month=models.CharField(max_length=100,unique="True",null=True)
  # fourg=models.CharField(max_length=100,default='0',null=True)
  # fiveg = models.CharField(max_length=100,  default='0' ,null=True)
  # cloud = models.CharField(max_length=100, default='0',null=True )
  # cloudcore = models.CharField(max_length=100,  default='0' ,null=True)
  # e2e = models.CharField(max_length=100,  default='0',null=True)
  # dx= models.CharField(max_length=100, default='0',null=True)
  # ece= models.CharField(max_length=100, default='0',null=True)
  # hetran= models.CharField(max_length=100, default='0',null=True )
  # sran= models.CharField(max_length=100,  default='0',null=True )


  def __str__(self):
  # return u'%s %s %s %s %s %s %s %s %s %s' % (self.month,self.fourg,  self.fiveg, self.cloud, self.cloudcore, self.e2e, self.dx,self.ece,self.hetran,self.sran,)
    return u'%s %s %s ' % (self.month,self.du,  self.num)

