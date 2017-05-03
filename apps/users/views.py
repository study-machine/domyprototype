# coding=utf-8
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from main.models import Prototype, Project
from users.models import *
from .forms import *
from utils.send_email import send_email


class CustomBackend(ModelBackend):
    # 重载登陆逻辑
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 使用Q使查询语句并集
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # AbstractUser的一个方法
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        sent = request.GET.get('sent', '')
        return render(request, 'usercenter/../../templates/users/login.html', {
            'sent': sent
        })

    def post(self, request):
        error_msg = ''
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            has_user = UserProfile.objects.filter(username=username) or UserProfile.objects.filter(email=username)
            if has_user:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    error_msg = u'密码错误'
            else:
                error_msg = u'用户不存在'
        else:
            error_msg = login_form.errors
        return self.login_error(request, error_msg)

    def login_error(self, request, error_msg):
        return render(request, 'users/login.html', {
            'error_msg': error_msg
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'usercenter/../../templates/users/register.html', {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        error_msg = ''
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email', '')
            password = register_form.cleaned_data.get('password', '')
            password2 = register_form.cleaned_data.get('password2', '')
            if UserProfile.objects.filter(email=email):
                error_msg = '邮箱已注册'
                return self.register_error(request, register_form, error_msg)
            if password != password2:
                error_msg = '两次输入密码不相等'
                return self.register_error(request, register_form, error_msg)
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_email(email, 'register')

            return HttpResponseRedirect(reverse('users:login') + '?sent=' + email)


        else:
            error_msg = register_form.errors
            return self.register_error(request, register_form, error_msg)

    def register_error(self, request, register_form, error_msg):
        return render(request, 'users/register.html', {
            'register_form': register_form,
            'error_msg': error_msg
        })


class ActivateUserView(View):
    def get(self, request, activate_code):
        all_codes_obj = EmailVerificationCode.objects.filter(code=activate_code, send_type='register')
        if all_codes_obj:
            for code_obj in all_codes_obj:
                user = UserProfile.objects.get(email=code_obj.email)
                user.is_active = True
                user.save()
            return render(request, 'users/activate_success.html', {})
        else:
            return render(request, 'users/activate_fail.html', {})


class MyPrototypeView(View):
    def get(self, request):
        prototypes = Prototype.objects.filter(user=request.user).order_by('-update_time')
        return render(request, 'usercenter/usercenter_myprototype.html', {
            'prototypes': prototypes,
        })


class MyProjectView(View):
    def get(self, request):
        projects = Project.objects.filter(user=request.user).order_by('-update_time')
        return render(request, 'usercenter/usercenter_myproject.html', {
            'projects': projects,
        })


class UserCenterView(View):
    def get(self, request):
        return render(request, 'usercenter/usercenter_profile.html', {})


class SendChangeEmail(View):
    def post(self, request):
        email = request.POST.get('email', 0)
        if not email:
            return self.return_error('请填写邮箱')
        try:
            validate_email(email)
        except ValidationError:
            return self.return_error('请输入正确邮箱格式')

        if send_email(email, 'update_email') != 1:
            return self.return_error('邮件发送失败')

        data = {
            'status': 'success',
            'request_user': request.user.username,
            'new_email': email
        }
        return JsonResponse(data)

    def return_error(self, error_msg):
        data = {
            'status': 'fail',
            'error_msg': error_msg
        }
        return JsonResponse(data)


class UpdateEmail(View):
    def post(self, request):
        verification_code = request.POST.get('code', 0)
        # 这里邮箱验证码中应该保存id比较好
        user_id = request.POST.get('userId', 0)
        all_codes_obj = EmailVerificationCode.objects.filter(code=verification_code, send_type='update_email')
        if all_codes_obj:
            for code_obj in all_codes_obj:
                user = UserProfile.objects.get(id=int(user_id))
                user.email = code_obj.email
                user.save()
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'error_msg': 'v_code not find'})
