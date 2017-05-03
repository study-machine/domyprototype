# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-06 17:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_project_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 3, 6, 17, 2, 46, 917108), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carousel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prototype',
            name='zip_file',
            field=models.FileField(upload_to='prototype/temp', verbose_name='\u539f\u578bzip\u5305'),
        ),
    ]
