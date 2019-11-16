#coding=utf-8

import xadmin

from .models import EmailVerifyRecord, Banner
from xadmin import views


# 可使用主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 修改页面的title 和 footer
class GlobalSettings(object):
    site_title = '装逼装用'
    site_footer = '状态专用网'
    # app可以进行展开收起
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    # 在后台系统中列表中显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 数据搜索
    search_fields = ['code', 'email', 'send_type']
    # 筛选
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 数据搜索
    search_fields = ['title', 'image', 'url', 'index']
    # 筛选
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 表注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
