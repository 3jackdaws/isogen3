# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 00:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0006_auto_20161229_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directoryentry',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='directoryentry',
            name='tags',
        ),
    ]
