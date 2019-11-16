#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/10/12 22:24'
from django.urls import path
from django.conf.urls import include, url
import xadmin
from django.views.generic import TemplateView

# 同于处理django的静态文件
from django.views.static import serve
from Mydjango.settings import MEDIA_ROOT
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, CourseAddCommentView, VideoPlayView

urlpatterns = [
    # 课程列表页
    url('^list/', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/', CourseAddCommentView.as_view(), name='course_add_comment'),
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]



