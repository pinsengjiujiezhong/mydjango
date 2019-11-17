#coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from opration.models import UserFavorite
from .froms import UserAskForm
from django.http import HttpResponse
from django.db.models import Q
from courses.models import Course
import json


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 教师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 城市筛选
        cityId = request.GET.get('city', '')
        if cityId:
            # 针对数据进行筛选
            all_orgs = all_orgs.filter(city_id=int(cityId))
        # 机构筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-course_nums')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-students')
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)
        org_nums = all_orgs.count()
        return render(request, 'org-list.html', {
            'org_nums': org_nums,
            'all_orgs': orgs,
            'citys': citys,
            'curr_cityId': cityId,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'search_keywords': search_keywords,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': '添加出错'}", content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_view = 'home'
        courses_org = CourseOrg.objects.get(id=int(org_id))
        courses_org.click_nums += 1
        courses_org.save()
        all_courses = courses_org.course_set.all()[:3]
        all_teachers = courses_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'courses_org': courses_org,
            'current_view': current_view

        })


class OrgCourseeView(View):
    def get(self, request, org_id):
        current_view = 'course'
        courses_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = courses_org.course_set.all()
        print('courses_org: ', courses_org.id)
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'courses_org': courses_org,
            'current_view': current_view
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_view = 'desc'
        courses_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'courses_org': courses_org,
            'current_view': current_view

        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_view = 'teacher'
        courses_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = courses_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'courses_org': courses_org,
            'current_view': current_view

        })


class AddFavView(View):
    # 用户收藏，和取消收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # if not request.user.is_authenticated():
        #     # 判断用户登录状态
        #     return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        # 使用用户、收藏id、收藏类型进行联合查询
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 记录已存在 表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:
            # 记录不存在 表示用户未收藏，并进行收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        curr_active = 'all'
        if request.GET.get('sort') == 'hot':
            all_teacher = all_teacher.order_by('-click_nums')
            curr_active = 'hot'

        # 教师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))

        sorted_teacher = all_teacher.order_by('-click_nums')[:3]
        # 对讲师机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 1, request=request)
        teachers = p.page(page)
        teacher_nums = all_teacher.count()
        return render(request, 'teachers-list.html', {
            'all_teacher': teachers,
            'curr_active': curr_active,
            'teacher_nums': teacher_nums,
            'sorted_teacher': sorted_teacher,
            'search_keywords': search_keywords,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(teacher_id=teacher_id)
        all_teacher = Teacher.objects.all()
        sorted_teacher = all_teacher.order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'sorted_teacher': sorted_teacher,
        })
