# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-09 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0004_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='activationString',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(default='mr', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName',
            field=models.CharField(default='xy', max_length=30),
            preserve_default=False,
        ),
    ]