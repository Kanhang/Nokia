# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-21 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subnet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subnet',
            name='snmp_version',
            field=models.CharField(choices=[('v2', 'v2'), ('v3', 'v3')], max_length=100, null=True),
        ),
    ]