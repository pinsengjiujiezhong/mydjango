#coding=utf-8
from django.db import models
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市')
    add_time = models.DateTimeField(default=datetime.now)
    desc = models.TextField(verbose_name=u'城市描述')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), verbose_name='机构类别', default='pxjg')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'logo')
    address = models.CharField(max_length=100, verbose_name=u'机构地址') #机构地址
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市', on_delete=models.CASCADE)  #城市外键
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_course_num(self):
        return self.course_set.all().count()

    def get_teacher_num(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'所属机构')
    name = models.CharField(max_length=10, verbose_name=u'教师名称')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限') #ImtegerField
    work_company = models.CharField(max_length=50, verbose_name=u'工作公司')
    work_postion = models.CharField(max_length=50, verbose_name=u'工作职位')#职位
    points = models.CharField(max_length=100, verbose_name=u'课程特点') #特点
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    age = models.IntegerField(default=0, verbose_name=u'年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_course_num(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
