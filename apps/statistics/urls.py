# -*- coding: utf-8 -*-
# @Time    : 17/5/6 下午10:29
# @Author  : wxy
# @File    : urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^launch_num/$', LauncherNumInChina.as_view(), name='launch_num'),
    url(r'^date_receipt/$', DateReceiptSum.as_view(), name='date_receipt'),
]
