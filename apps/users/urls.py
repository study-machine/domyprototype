# -*- coding: utf-8 -*-
# @Time    : 17/3/3 下午5:12
# @Author  : wxy
# @File    : urls.py

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<activate_code>.*)/$', ActivateUserView.as_view(), name='activate_user'),
    url(r'^update_email/$', UpdateEmail.as_view(), name='update_email'),
    url(r'^user_center/$', UserCenterView.as_view(), name='user_center'),
    url(r'^my_prototype/$', MyPrototypeView.as_view(), name='my_prototype'),
    url(r'^my_project/$', MyProjectView.as_view(), name='my_project'),
    url(r'^send_change_email/$', SendChangeEmail.as_view(), name='send_change_email'),
    url(r'^update_nickname/$', UpdateNickName.as_view(), name='update_nickname'),
]
