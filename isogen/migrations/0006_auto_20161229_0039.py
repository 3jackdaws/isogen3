# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0005_auto_20161229_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoryentry',
            name='logo',
            field=models.ImageField(upload_to='directory-images'),
        ),
        migrations.AlterField(
            model_name='directoryentry',
            name='picture',
            field=models.ImageField(upload_to='directory-images'),
        ),
    ]