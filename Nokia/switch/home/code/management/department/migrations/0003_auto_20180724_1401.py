# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 06:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_auto_20180724_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='DU',
            new_name='Tribe_name',
        ),
    ]
