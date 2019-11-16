"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include, url
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveView, ForGetPwdView, ResetView, ModifyPwdView, UserLoginView
from organization.views import OrgView
# 同于处理django的静态文件
from django.views.static import serve
from Mydjango.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url('^login/', LoginView.as_view(), name='login'),
    url('^login/', UserLoginView.as_view(), name='login'),
    url('^register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='active'),
    url('^forget/', ForGetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pass'),
    url('^modify/', ModifyPwdView.as_view(), name='modify'),
    # 课程机构url 配置
    url(r'^org/', include(('organization.urls', 'organization'), namespace='org')),

    # 课程机构url 配置
    url(r'^course/', include(('courses.urls', 'courses'), namespace='courses')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 课程机构url配置

    # 个人中心url配置
    url(r'^users/', include(('users.urls', 'users'), namespace='users')),
]
