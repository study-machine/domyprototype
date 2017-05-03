# -*- coding: utf-8 -*-
# @Time    : 17/3/3 下午1:49
# @Author  : wxy
# @File    : forms.py

from django import forms

from main.models import Prototype, Project


class UploadForm(forms.ModelForm):
    class Meta:
        model = Prototype
        fields = ['name', 'project', 'detail', 'zip_file', 'image']


class EditForm(forms.ModelForm):
    class Meta:
        model = Prototype
        fields = ['name', 'project', 'detail', 'image']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'detail']
