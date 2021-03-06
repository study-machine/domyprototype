# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateReceiptStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('app_sum', models.IntegerField(blank=True, null=True)),
                ('premiere_sum', models.IntegerField(blank=True, null=True)),
                ('vip_sum', models.IntegerField(blank=True, null=True)),
                ('pack_sum', models.IntegerField(blank=True, null=True)),
                ('recharge_sum', models.IntegerField(blank=True, null=True)),
                ('total_sum', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': '\u65e5\u6536\u6b3e\u7edf\u8ba1',
                'verbose_name_plural': '\u65e5\u6536\u6b3e\u7edf\u8ba1',
            },
        ),
    ]
