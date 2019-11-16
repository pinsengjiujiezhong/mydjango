#coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course, Lesson, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from opration.models import UserFavorite, CourseComments, UserCourse, CourseComments, UserCourse
from organization.models import CityDict
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        print('all_course: ', all_course)
        hot_courses = Course.objects.all().order_by('-students')
        if len(hot_courses) >= 3:
            hot_courses = hot_courses[:3]
        # 排序
        sort = request.GET.get('sort', '')

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        if sort == 'students':
            all_course = all_course.order_by('-students')
        elif sort == 'hot':
            all_course = all_course.order_by('-fav_nums')
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)
        courses = p.page(page)
        print('courses: ', courses)
        org_nums = all_course.count()
        return render(request, 'course-list.html', {
            'all_course': all_course,
            'sort': sort,
            'hot_courses': hot_courses,
            'search_keywords': search_keywords,
        })


class CourseDetailView(View):
    # 课程详情页
    def get(self, request, course_id):
        print(course_id)
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        # 课程详情页收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        print(' course.tags: ',  course.tags)
        if course.tags:
            recommended_courses = Course.objects.filter(tags=course.tags)
            if recommended_courses[0] == course:
                recommended_courses = recommended_courses[1:2]
            else:
                recommended_courses = recommended_courses[:1]
        else:
            recommended_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'recommended_courses': recommended_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        all_lessons = Lesson.objects.filter(courses_id=course_id)
        curr_course = Course.objects.get(id=course_id)
        all_video = Video.objects.filter(courses_id=course_id)
        all_lesson_id = Lesson.objects.filter(courses_id=course_id).values('id')
        user_courses = UserCourse.objects.filter(course_id=course_id)
        user_ids = [user.id for user in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.course_id for course in all_courses]
        resource_courses = Course.objects.filter(id__in=course_ids)[:3]
        return render(request, 'course-video.html', {
            'all_lessons': all_lessons,
            'curr_course': curr_course,
            'resource_courses': resource_courses,
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        curr_course = Course.objects.get(id=course_id)
        all_comments = CourseComments.objects.all().order_by('-add_time')
        user_courses = UserCourse.objects.filter(course_id=course_id)
        user_ids = [user.id for user in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.course_id for course in all_courses]
        resource_courses = Course.objects.filter(id__in=course_ids)[:3]
        return render(request, 'course-comment.html', {
            'curr_course': curr_course,
            'all_comments': all_comments,
            'resource_courses': resource_courses
        })


class CourseAddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"error", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course_id = video.courses_id
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        all_lessons = Lesson.objects.filter(courses_id=course_id)
        curr_course = Course.objects.get(id=course_id)
        all_video = Video.objects.filter(courses_id=course_id)
        all_lesson_id = Lesson.objects.filter(courses_id=course_id).values('id')
        user_courses = UserCourse.objects.filter(course_id=course_id)
        user_ids = [user.id for user in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.course_id for course in all_courses]
        resource_courses = Course.objects.filter(id__in=course_ids)[:3]
        return render(request, 'course-play.html', {
            'all_lessons': all_lessons,
            'course': curr_course,
            'resource_courses': resource_courses,
            'video': video,
        })

