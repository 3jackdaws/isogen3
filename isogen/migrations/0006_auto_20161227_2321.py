# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 23:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen', '0005_auto_20161227_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberlinkedaccounts',
            name='linked_account',
        ),
        migrations.RemoveField(
            model_name='memberlinkedaccounts',
            name='member',
        ),
        migrations.RemoveField(
            model_name='file',
            name='filename',
        ),
        migrations.AlterField(
            model_name='file',
            name='members_allowed',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='LinkedAccounts',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='MemberLinkedAccounts',
        ),
    ]
