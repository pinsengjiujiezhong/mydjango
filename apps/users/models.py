# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 用户model，继承了Django原有用户表中的字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(('male', u'男'),  ('female', u"女")), default='male')
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(default=None, max_length=11, null=True, blank=True)
    # 使用imagefield时需要pillow库
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)
    is_active = models.IntegerField(default=0)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def get_user_course(self):
        return self.usercourse_set.all()

    def get_unread_num(self):
        return self.usermessage_set.count()

    def __str__(self):
        return self.username

# verbose_name=u'验证码类型' 这个会直接在后台显示相关的名称
# 邮箱验证码model


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u'验证码类型', choices=(("register", u"注册"), ("forget", u"找回密码"),
                                                                ("update_email", u"修改邮箱" )), max_length=15)
    # now加括号会根据model生成时的时间，不加括号会根据生成实例的时间
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 当前是设置后台管理系统中数据显示格式
        # return '{code}({email})'.format(self.code, self.email)
        return '{0}({1})'.format(self.code, self.email)


# 轮播图model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name



