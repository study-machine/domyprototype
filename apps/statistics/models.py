# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class DateReceiptStatistics(models.Model):
    date = models.DateField(unique=True)
    app_sum = models.IntegerField(blank=True, null=True)
    premiere_sum = models.IntegerField(blank=True, null=True)
    vip_sum = models.IntegerField(blank=True, null=True)
    pack_sum = models.IntegerField(blank=True, null=True)
    recharge_sum = models.IntegerField(blank=True, null=True)
    total_sum = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = u'日收款统计'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __unicode__(self):
        from datetime import datetime
        return datetime.strftime(self.date, '%Y-%m-%d') + ':' + str(self.total_sum)