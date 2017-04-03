# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0003_auto_20170105_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIConsumer',
            fields=[
                ('identifier', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='url',
            field=models.CharField(default='file', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apiconsumer',
            name='permissions',
            field=models.ManyToManyField(to='isogen.Permission'),
        ),
    ]
