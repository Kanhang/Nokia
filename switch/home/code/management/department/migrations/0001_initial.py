# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DU', models.CharField(blank=True, max_length=100, null=True)),
                ('Tribe', models.EmailField(max_length=100)),
                ('Squad_groups', models.EmailField(max_length=100)),
                ('Squad', models.EmailField(max_length=100)),
                ('LabOps', models.EmailField(max_length=100)),
                ('LabOrder', models.EmailField(max_length=100)),
                ('LabSupport', models.EmailField(max_length=100)),
            ],
        ),
    ]
