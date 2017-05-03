# -*- coding: utf-8 -*-
# @Time    : 17/5/3 下午3:13
# @Author  : wxy
# @File    : urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^introduction/$', IntroductionView.as_view(), name='introduction'),
]
