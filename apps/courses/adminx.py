#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/8/25 15:50'

from .models import Course, Lesson, Video, CourseResource

import xadmin


class CourseAdmin(object):
    # 在后台系统中列表中显示的列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    # 数据搜索
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    # 筛选
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']


class LessonAdmin(object):
    # 在后台系统中列表中显示的列
    list_display = ['name', 'courses', 'add_time']
    # 数据搜索  均需要使用外键   courses__name
    search_fields = ['courses__name', 'name']
    # 筛选  courses__name  courses的name字段   外键的处理方式
    list_filter = ['courses__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    # 数据搜索
    search_fields = ['lesson__name', 'name']
    # 筛选
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    # 在后台系统中列表中显示的列
    list_display = ['course', 'name', 'download', 'add_time']
    # 数据搜索
    search_fields = ['course__name', 'name', 'download']
    # 筛选
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)