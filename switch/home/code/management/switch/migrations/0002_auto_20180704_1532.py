# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-04 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='Snmpv3',
            field=models.CharField(max_length=100, null=True),
        ),
    ]