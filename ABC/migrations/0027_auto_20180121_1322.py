# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-21 13:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABC', '0026_auto_20180121_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.datetime),
        ),
        migrations.AlterField(
            model_name='task',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='notice_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
