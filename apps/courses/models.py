#coding=utf-8

from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='课程名称', max_length=50, default='1')
    desc = models.CharField(verbose_name='课程描述', max_length=200, default='1')
    detail = models.TextField(verbose_name='课程详情', max_length=200, default='1')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), verbose_name='课程难度', max_length=10, default='中级')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'logo')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.IntegerField(default="后端开发", verbose_name='课程类别')
    tags = models.CharField(default="", verbose_name='课程标记', max_length=20)
    teacher = models.ForeignKey(Teacher, verbose_name='讲课老师', null=True, on_delete=models.CASCADE, default='1')
    instructions = models.CharField(max_length=200, default='', verbose_name='课程须知')
    learning = models.CharField(max_length=200, default='', verbose_name='能学到什么')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_chapter_num(self):
        chapter_num = self.lesson_set.all().count()
        return chapter_num

    def get_learn_users(self):
        return self.usercourse_set.all()

    def get_course_resource(self):
        return self.courseresource_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    # 外键关联
    courses = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_videos(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    # 外键关联
    courses = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'视频名',  default='')
    url = models.CharField(max_length=200, verbose_name=u'播放链接', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    # 外键关联
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='名称', default='')
    download = models.FileField(upload_to='courses/resource/%Y%m', verbose_name='下载链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name