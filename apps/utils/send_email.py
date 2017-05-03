# -*- coding: utf-8 -*-
# @Time    : 17/4/14 下午4:42
# @Author  : wxy
# @File    : send_email.py
from random import randint

from django.core.mail import send_mail

from users.models import EmailVerificationCode
from domyprototype.settings import EMAIL_FROM, PRODUCTION


def generate_random_str(random_length=16):
    ran_str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars)
    for i in range(random_length):
        ran_str += chars[randint(0, length - 1)]
    return ran_str


def send_email(email, send_type):
    if PRODUCTION:
        host_name = 'www.wangxiyang.com'
    else:
        host_name = '127.0.0.1:8000'

    if send_type == 'register':
        code = generate_random_str()
        email_title = '家视天下产品平台－激活链接邮件'
        email_body = '请点击下面的链接激活你的账号:http://{0}/users/activate/{1}'.format(host_name, code)
    elif send_type == 'forget':
        code = generate_random_str()
        email_title = '家视天下产品平台修改'
        email_body = '请点击下面的链接更改您的密码:http://{0}/users/activate/{1}'.format(host_name, code)
    elif send_type == 'update_email':
        code = generate_random_str(6)
        email_title = '家视天下产品平台邮件'
        email_body = '请使用验证码，修改邮箱，验证码：{0}'.format(code)

    try:
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    except Exception, e:
        print e
        return
    # 邮箱验证码入库
    email_code = EmailVerificationCode()
    email_code.code = code
    email_code.email = email
    email_code.send_type = send_type
    email_code.save()

    return send_status
