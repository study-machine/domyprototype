from django.test import TestCase

from django.core.mail import send_mail

# postmaster@wangxiyang.com

send_mail('Subject here', 'Here is the message. test', 'study_machine@163.com', ['wangxiyang1@btte.net', 'brook45@163.com'],
          fail_silently=False)
