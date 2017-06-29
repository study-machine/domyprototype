# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-22 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u57ce\u5e02')),
                ('jd', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='\u7ecf\u5ea6')),
                ('wd', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='\u7eac\u5ea6')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='\u7701\u4efd')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statistics.Province', verbose_name='\u7701\u4efd'),
        ),
    ]
