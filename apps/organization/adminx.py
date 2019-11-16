#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/8/25 20:51'

from .models import CityDict, CourseOrg, Teacher
import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    # 在后台系统中列表中显示的列
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    # 数据搜索
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city__name']
    # 筛选
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city__name', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org__name', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)




