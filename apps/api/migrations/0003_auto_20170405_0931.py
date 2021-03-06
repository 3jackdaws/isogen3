# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_apiaccessrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIConsumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_created=True)),
                ('token', models.CharField(max_length=32)),
                ('token_date', models.DateTimeField()),
                ('identifier', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='apiaccessrecord',
            name='response_time',
        ),
        migrations.AddField(
            model_name='apiaccessrecord',
            name='consumer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.APIConsumer'),
            preserve_default=False,
        ),
    ]
