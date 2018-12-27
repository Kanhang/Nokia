# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-20 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='subnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subnet', models.CharField(max_length=100, null=True)),
                ('du', models.CharField(default='', max_length=100, null=True)),
                ('location', models.CharField(default='', max_length=100, null=True)),
                ('snmp_version', models.CharField(default='', max_length=100, null=True)),
                ('Community', models.CharField(blank=True, max_length=100, null=True)),
                ('Username', models.CharField(blank=True, max_length=100, null=True)),
                ('Password', models.CharField(blank=True, max_length=100, null=True)),
                ('Authority', models.CharField(blank=True, max_length=100, null=True)),
                ('Authentication_protocol', models.CharField(blank=True, max_length=100, null=True)),
                ('privacy_protocol', models.CharField(blank=True, max_length=100, null=True)),
                ('Passphase', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
    ]
