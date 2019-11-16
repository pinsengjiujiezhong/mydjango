#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/8/31 14:57'
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
import random
from Mydjango.settings import EMAIL_FROM


def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str


def email_send(email, send_type='register'):
    email_verify = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_verify.code = code
    email_verify.email = email
    if send_type == 'register':
        email_verify.send_type = 'register'
        email_verify.save()
        email_title = '当前注册的邮件'
        email_body = '这个也是注册的邮件链接 http://127.0.0.1:8000/active/{code}'.format(code=code)
    if send_type == 'forget':
        email_verify.send_type = 'forget'
        email_verify.save()
        email_title = '当前重置密码的邮件'
        email_body = '这个是重置密码的链接 http://127.0.0.1:8000/reset/{code}'.format(code=code)
    if send_type == 'update_email':
        email_verify.send_type = 'update_email'
        email_verify.save()
        email_title = '当前修改邮箱的邮件'
        email_body = '这个是修改邮箱的验证码：{code}'.format(code=code)
    email_form = EMAIL_FROM
    email_list = [email]
    send_status = send_mail(email_title, email_body, email_form, email_list)
    return send_status
