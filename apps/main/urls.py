# -*- coding: utf-8 -*-
# @Time    : 17/3/6 上午10:58
# @Author  : wxy
# @File    : urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    # 原型
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^prototype_detail/(?P<prototype_id>\d+)/$', PrototypeDetailView.as_view(), name='prototype_detail'),
    url(r'^prototype_edit/(?P<prototype_id>\d+)/$', PrototypeEditView.as_view(), name='prototype_edit'),
    url(r'^prototype_delete/(?P<prototype_id>\d+)/$', PrototypeDeleteView.as_view(), name='prototype_delete'),
    url(r'^prototype_list/$', PrototypeListView.as_view(), name='prototype_list'),

    # 项目
    url(r'^add_project/$', AddProjectView.as_view(), name='add_project'),
    url(r'^project_list/$', ProjectListView.as_view(), name='project_list'),
    url(r'^project_detail/(?P<project_id>\d+)/$', ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project_edit/(?P<project_id>\d+)/$', ProjectEditView.as_view(), name='project_edit'),
    url(r'^project_delete/(?P<project_id>\d+)/$', ProjectDeleteView.as_view(), name='project_delete'),

]
