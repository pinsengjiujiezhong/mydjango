#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/11/2 22:24'
from django.urls import path
from django.conf.urls import include, url
import xadmin
from django.views.generic import TemplateView
from .views import UsersInfoView, UserUploadView, UpdateModifyPwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView, UserLoginView
# 同于处理django的静态文件
from django.views.static import serve
from Mydjango.settings import MEDIA_ROOT

urlpatterns = [
    url('^info/$', UsersInfoView.as_view(), name='users_center'),
    url('^image/upload/$', UserUploadView.as_view(), name='users_upload'),
    url('^update/pwd/$', UpdateModifyPwdView.as_view(), name='user_update_pwd'),
    # 发送邮箱验证码
    url('^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url('^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url('^my_course/$', MyCourseView.as_view(), name='users_course'),

    # 我收藏的课程机构
    url('^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 我收藏的授课教师
    url('^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我收藏的课程
    url('^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 我的消息
    url('^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]



