# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='Type',
        ),
        migrations.AddField(
            model_name='device',
            name='DU',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='Device_type',
            field=models.CharField(blank=True, choices=[('Switch', 'Switch'), ('Server', 'Server'), ('PB', 'PB')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='Status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='Update_time',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]