# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 09:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20161027_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 27, 9, 58, 44, 571218, tzinfo=utc)),
        ),
    ]
