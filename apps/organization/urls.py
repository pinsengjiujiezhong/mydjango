#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/9/8 22:24'
from django.urls import path
from django.conf.urls import include, url
import xadmin
from django.views.generic import TemplateView
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseeView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView
# 同于处理django的静态文件
from django.views.static import serve
from Mydjango.settings import MEDIA_ROOT

urlpatterns = [
    url('^list/', OrgView.as_view(), name='org_list'),
    url('^add_ask/', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>.*)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>.*)/$', OrgCourseeView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>.*)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>.*)/$', OrgTeacherView.as_view(), name='org_teacher'),
    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    # 讲师列表
    url(r'^teachers/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 讲师详情
    url(r'^teachers/detail/(?P<teacher_id>.*)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]



