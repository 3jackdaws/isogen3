# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0008_auto_20161229_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoryentry',
            name='icon',
            field=models.CharField(default='fa-leaf', max_length=32),
        ),
    ]
