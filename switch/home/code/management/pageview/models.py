# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here
class page(models.Model):
  page_index_count = models.IntegerField(null=True,default=0, help_text="page_index_count")
  refresh_count = models.IntegerField(null=True,default=0, help_text="refresh_count")
  class Meta:
    app_label = "pageview"  