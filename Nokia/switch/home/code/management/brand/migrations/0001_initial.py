# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-20 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(default='', max_length=100, null=True)),
                ('num', models.CharField(default='', max_length=100, null=True)),
            ],
        ),
    ]
