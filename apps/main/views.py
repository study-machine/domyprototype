# coding=utf-8
import zipfile
import os

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import *
from utils.utils import unzip_file, remove_prototype_dir


class IndexView(View):
    def get(self, request):
        carousels = Carousel.objects.filter(active=True).order_by('order')[:3]
        prototypes = Prototype.objects.all()[:12]
        return render(request, 'index.html', {
            'carousels': carousels,
            'prototypes': prototypes,
        })


class UploadView(View):
    def get(self, request):
        if request.user.is_authenticated():
            projects = Project.objects.filter(user=request.user)
        else:
            projects = None
        return render(request, 'prototype/prototype_upload.html', {
            'projects': projects,
        })

    def post(self, request):
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.instance.user = request.user
            upload_form.save()
            full_filename = upload_form.instance.zip_file.file.name
            prototype_id = upload_form.instance.id

            # 解压缩，放在media下面，上传者username文件夹下的目录
            is_unzipped, result = unzip_file(full_filename, request.user.username, prototype_id)
            # 是否压缩成功
            if is_unzipped:
                # 保存index_url到数据库
                upload_form.instance.index_url = result
                upload_form.save()

                return HttpResponseRedirect(reverse('main:prototype_detail', kwargs={'prototype_id': prototype_id}))
            else:
                error_msg = '包解压或解析失败，请检查打包方式(打包的文件夹要使用英文，文件夹中要有index.html)。\n'
                error_msg += result
        else:
            error_msg = upload_form.errors

        # 提交错误，表单回填
        projects = Project.objects.filter(user=request.user)
        project_id = upload_form.cleaned_data['project'].id
        prototype_name = request.POST.get('name')
        return render(request, 'prototype/prototype_upload.html', {
            'error_msg': error_msg,
            'projects': projects,
            'prototype_name': prototype_name,
            'project_id': project_id,
        })


class AddProjectView(View):
    def get(self, request):
        projects = Prototype.objects.filter(user=request.user)
        return render(request, 'project/project_add.html', {
            'projects': projects
        })

    def post(self, request):
        error_msg = ''
        add_project_form = ProjectForm(request.POST)
        if add_project_form.is_valid():
            add_project_form.instance.user = request.user
            add_project_form.save()
            return HttpResponseRedirect(reverse('main:upload'))
        else:
            error_msg = add_project_form.errors
        return render(request, 'project/project_add.html', {
            'error_msg': error_msg
        })


class PrototypeDetailView(View):
    def get(self, request, prototype_id):
        prototype = Prototype.objects.get(id=int(prototype_id))
        return render(request, 'prototype/prototype_detail.html', {
            'prototype': prototype
        })


class PrototypeListView(View):
    def get(self, request):
        prototypes = Prototype.objects.all()

        # 搜索
        search_keyword = request.GET.get('keyword', '')
        if search_keyword:
            prototypes = prototypes.filter(Q(name__icontains=search_keyword) |
                                           Q(detail__icontains=search_keyword) |
                                           Q(project__name__icontains=search_keyword) |
                                           Q(user__nick_name__icontains=search_keyword))

        # 分页
        paginator = Paginator(prototypes, 20)

        current_page = request.GET.get('page')
        try:
            prototypes = paginator.page(current_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            prototypes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            prototypes = paginator.page(paginator.num_pages)

        return render(request, 'prototype/prototype_list.html', {
            'prototypes': prototypes,
            'search_keyword': search_keyword,
        })


class PrototypeEditView(View):
    def get(self, request, prototype_id):
        prototype = Prototype.objects.get(id=int(prototype_id))
        projects = Project.objects.filter(user=request.user)
        return render(request, 'prototype/prototype_edit.html', {
            'prototype': prototype,
            'projects': projects,
        })

    def post(self, request, prototype_id):
        edit_form = EditForm(request.POST, request.FILES)
        if edit_form.is_valid():
            prototype = Prototype.objects.get(id=int(prototype_id))
            prototype.name = edit_form.cleaned_data['name']
            prototype.detail = edit_form.cleaned_data['detail']
            prototype.project = edit_form.cleaned_data['project']
            if edit_form.cleaned_data['image']:
                prototype.image = edit_form.cleaned_data['image']
            prototype.save()

        return HttpResponseRedirect(reverse('main:prototype_detail', kwargs={'prototype_id': prototype_id}))


class PrototypeDeleteView(View):
    def get(self, request, prototype_id):
        prototype = Prototype.objects.get(id=int(prototype_id))
        if request.user == prototype.user:
            prototype.delete()
            remove_prototype_dir(request.user.username, prototype_id)
            return HttpResponseRedirect(reverse('users:my_prototype'))
        else:
            return HttpResponseRedirect(reverse('users:my_prototype'))



class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=int(project_id))
        prototypes = Prototype.objects.filter(project=project.id)
        return render(request, 'project/project_detail.html', {
            'prototypes': prototypes,
            'project': project,

        })


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'project/project_list.html', {
            'projects': projects,
        })


class ProjectEditView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=int(project_id))
        return render(request, 'project/project_edit.html', {
            'project': project,
        })

    def post(self, request, project_id):
        project_form = ProjectForm(request.POST)
        project = Project.objects.get(int(project_id))
        if project_form.is_valid():
            project.name = project_form.cleaned_data['name']
            project.detail = project_form.cleaned_data['detail']
            project.save()
            return HttpResponseRedirect(reverse('main:project_detail', kwargs={'project_id': project_id}))
        else:
            error_msg = project_form.errors
            return render(request, 'project/project_edit.html', {
                'project': project,
                'error_msg': error_msg
            })


class ProjectDeleteView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=int(project_id))
        if request.user == project.user:
            if project.get_prototype_number() == 0:
                project.delete()
                return HttpResponseRedirect(reverse('users:my_project'))
            else:
                error_msg = '只能删除原型为0的项目'
        else:
            error_msg = '只能删除用户自己的项目 '
        projects = Project.objects.filter(user=request.user).order_by('-update_time')
        return render(request, 'usercenter/usercenter_myproject.html', {
            'projects': projects,
            'error_msg': error_msg,
        })
