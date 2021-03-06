# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-04 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IPAddress', models.CharField(max_length=100, null=True, unique=True)),
                ('Type', models.CharField(blank=True, max_length=100, null=True)),
                ('Model', models.CharField(blank=True, max_length=100, null=True)),
                ('Version', models.CharField(blank=True, max_length=100, null=True)),
                ('DU', models.CharField(max_length=100, null=True)),
                ('Name', models.CharField(blank=True, max_length=100, null=True)),
                ('Location', models.CharField(max_length=100, null=True)),
                ('BackupFailed', models.CharField(blank=True, max_length=100, null=True)),
                ('Last_backup_date', models.CharField(blank=True, max_length=100, null=True)),
                ('Online', models.BooleanField(default=False)),
                ('Stdname', models.BooleanField(default=False)),
                ('Runtime', models.CharField(blank=True, max_length=100, null=True)),
                ('snmp_version', models.CharField(blank=True, choices=[('v2c', 'v2c'), ('v3', 'v3')], max_length=100, null=True)),
                ('Community', models.CharField(blank=True, max_length=100, null=True)),
                ('Username', models.CharField(blank=True, max_length=100, null=True)),
                ('Password', models.CharField(blank=True, max_length=100, null=True)),
                ('Authority', models.CharField(blank=True, choices=[('noAuthNoPriv', 'noAuthNoPriv'), ('authNoPriv', 'authNoPriv'), ('authPriv', 'authPriv')], max_length=100, null=True)),
                ('Authentication_protocol', models.CharField(blank=True, choices=[('MD5', 'MD5'), ('SHA', 'SHA')], max_length=100, null=True)),
                ('privacy_protocol', models.CharField(blank=True, choices=[('DES', 'DES'), ('AES', 'AES')], max_length=100, null=True)),
                ('Passphase', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Snmpv3', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': "switches' info",
                'verbose_name_plural': "switches' info",
            },
        ),
    ]
