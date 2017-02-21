# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='isogenmember',
            name='image',
            field=models.ImageField(blank=True, upload_to='members'),
        ),
        migrations.AlterField(
            model_name='isogenmember',
            name='bio',
            field=models.CharField(blank=True, default=None, max_length=1200),
        ),
    ]
