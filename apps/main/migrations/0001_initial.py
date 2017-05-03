# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-05 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel_type', models.IntegerField(choices=[(1, '\u94fe\u63a5'), (2, '\u539f\u578b\u8be6\u60c5')], verbose_name='\u8f6e\u64ad\u56fe\u7c7b\u578b')),
                ('image_url', models.CharField(max_length=256, verbose_name='\u56fe\u7247\u94fe\u63a5')),
                ('title', models.CharField(max_length=64, verbose_name='\u8f6e\u64ad\u56fe\u6807\u9898')),
                ('sub_title', models.CharField(max_length=64, verbose_name='\u8f6e\u64ad\u56fe\u526f\u6807\u9898')),
                ('active', models.BooleanField(verbose_name='\u662f\u5426\u751f\u6548')),
            ],
            options={
                'verbose_name': '\u8f6e\u64ad\u56fe',
                'verbose_name_plural': '\u8f6e\u64ad\u56fe',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1\u9879\u76ee',
                'verbose_name_plural': '\u4ea7\u54c1\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='\u539f\u578b\u540d\u79f0')),
                ('index_url', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u9996\u9875\u5730\u5740')),
                ('zip_file', models.FileField(blank=True, null=True, upload_to='prototype/temp', verbose_name='\u539f\u578bzip\u5305')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='\u8bf4\u660e')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/%Y/%m', verbose_name='\u539f\u578b\u56fe\u7247')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Project', verbose_name='\u6240\u5c5e\u9879\u76ee')),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1\u539f\u578b',
                'verbose_name_plural': '\u4ea7\u54c1\u539f\u578b',
            },
        ),
    ]
