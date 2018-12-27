# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class department(models.Model):
    Tribe_name = models.CharField(max_length=100,null=True)
    Tribe = models.EmailField(max_length=100)
    Squad_groups = models.EmailField(max_length=100)
    Squad = models.EmailField(max_length=100)
    LabOps = models.EmailField(max_length=100)
    LabOrder = models.EmailField(max_length=100)
    LabSupport = models.EmailField(max_length=100)

    def __str__(self):
        return u'%s' % (self.Tribe_name)

