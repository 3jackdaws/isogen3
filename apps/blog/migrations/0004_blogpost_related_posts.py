# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='related_posts',
            field=models.ManyToManyField(blank=True, to='blog.BlogPost'),
        ),
    ]
