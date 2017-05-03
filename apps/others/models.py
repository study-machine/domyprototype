# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Version(models.Model):
    version_number = models.CharField(max_length=10, verbose_name=u'版本号')
    desc = models.TextField(blank=True, null=True, verbose_name=u'说明')
    version_update_time = models.DateTimeField(blank=True, null=True, verbose_name=u'版本升级时间')

    class Meta:
        verbose_name = u'版本'
        verbose_name_plural = verbose_name
        ordering = ['-version_update_time']

    def __unicode__(self):
        return self.version_number
