# -*- coding: utf-8 -*-
# @Time    : 17/3/3 下午5:20
# @Author  : wxy
# @File    : forms.py
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

