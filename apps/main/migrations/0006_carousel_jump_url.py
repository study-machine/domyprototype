# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-06 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_carousel_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='jump_url',
            field=models.CharField(default='', max_length=256, verbose_name='\u8df3\u8f6c\u94fe\u63a5'),
        ),
    ]
