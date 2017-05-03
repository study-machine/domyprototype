# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from users.models import UserProfile


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'项目名称')
    user = models.ForeignKey(UserProfile, verbose_name=u'所属用户')
    detail = models.TextField(verbose_name=u'说明', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'产品项目'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

    def __unicode__(self):
        return self.name

    def get_prototype_number(self):
        return self.prototype_set.all().count()


class Prototype(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'原型名称')
    user = models.ForeignKey(UserProfile, verbose_name=u'所属用户')
    index_url = models.CharField(max_length=128, verbose_name=u'首页地址', blank=True, null=True)
    zip_file = models.FileField(upload_to='prototype/temp', verbose_name=u'原型zip包')
    project = models.ForeignKey(Project, verbose_name=u'所属项目', blank=True, null=True)
    detail = models.TextField(verbose_name=u'说明', blank=True, null=True)
    image = models.ImageField(verbose_name=u'原型图片', upload_to='image/%Y/%m', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'产品原型'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

    def __unicode__(self):
        return self.name


class Carousel(models.Model):
    TYPE_CHOICES = (
        (1, u'链接'),
        (2, u'原型详情'),
    )
    carousel_type = models.IntegerField(verbose_name=u'轮播图类型', choices=TYPE_CHOICES)
    image_url = models.CharField(verbose_name=u'图片链接', max_length=256)
    title = models.CharField(max_length=64, verbose_name=u'轮播图标题')
    sub_title = models.CharField(max_length=64, verbose_name=u'轮播图副标题')
    active = models.BooleanField(verbose_name=u'是否生效')
    order = models.IntegerField(verbose_name=u'显示顺序', default=99)
    jump_url = models.CharField(verbose_name=u'跳转链接', max_length=256, default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
