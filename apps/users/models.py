# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=64, verbose_name=u'昵称', default='')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerificationCode(models.Model):
    SEND_TYPE_CHOICES = (('register', u'注册'),
                         ('forget', u'找回密码'),
                         ('update_email', u'修改邮箱'))
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=15, verbose_name=u'验证码类型',
                                 choices=SEND_TYPE_CHOICES)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)
