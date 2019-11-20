#coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Banner
from opration.models import UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from django.db.models import Q
from django.views.generic.base import View
from .froms import LoginForm, RegisterForm, ForGetPwdForm, ResetForm, UserUploadForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import email_send
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
# 链接重定向  HttpResponseRedirect


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # | 为并集  , 为交集
            # 当前会同时查询2个字段 username和email,只要一个是正确的就可以
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print('e: ', e)
            return None


class ForGetPwdView(View):
    def get(self, request):
        return render(request, 'forgetpwd.html')

    def post(self, request):
        forget_form = ForGetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            code = email_send(email, 'forget')
            return render(request, 'send_success.html', {'forget_form': forget_form})
        else:
            return render(request, 'forgetpwd.html', {'msg': '数据填写错误'})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(username=email):
                return render(request, 'register.html', {'msg': '用户已经注册'})
            password = request.POST.get('password', '')
            captcha = request.POST.get('captcha', '')
            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password)
            user.save()

            # 写入注册得消息
            user_message = UserMessage()
            user_message.user_id = user.id
            user_message.has_read = '欢迎注册慕学在线网'
            user_message.save()

            send_status = email_send(email, 'register')
            print('send_status: ', send_status)
            return render(request, 'login.html')
        else:
            print('register_form: ', register_form.errors)
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_verify = EmailVerifyRecord.objects.filter(code=active_code)
        if all_verify:
            for verify in all_verify:
                email = verify.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


# 当前会自己调用，get模式会调用get，post会自动调用post
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # 检查form中的数据是否合法
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 检查数据正确性
            user = authenticate(username=user_name, password=pass_word)
            if user:
                userdb = UserProfile.objects.get(username=user_name)
                if userdb.is_active:
                    login(request, user)
                    db_code = UserProfile.objects.filter(username=user_name)
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 退出登录
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


# 测试sql 注入
class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        import pymysql
        db = pymysql.connect("localhost", "root", "root", "mydjango")
        cursor = db.cursor()
        sql = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name, pass_word)
        cursor.execute(sql)
        for data in cursor.fetchall():
            print(data)
        return render(request, 'index.html', {})


class ResetView(View):
    def get(self, request, reset_code):
        all_verify = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_verify:
            for verify in all_verify:
                email = verify.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'reset.html', {'email': email})
        else:
            return render(request, 'reset.html', {'msg': '邮箱未找到'})


class ModifyPwdView(View):
    """
    用户修改密码
    """
    def post(self, request):
        modify_forms = ResetForm(request.POST)
        if modify_forms.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'reset.html', {'msg': '两次密码不匹配'})
            email = request.POST.get('email', '')
            user = UserProfile.objects.get(username=email)
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'reset.html', {'modify_forms': modify_forms})


class UsersInfoView(LoginRequiredMixin, View):
    """
    用户信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_from = UserInfoForm(request.POST, instance=request.user)
        print('user_from: ', user_from.initial['birday'])
        print('type: ', type(user_from.initial['birday']))
        if user_from.is_valid():
            user_from.save()
            dict = {'status': 'success'}
            return HttpResponse(json.dumps(dict), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_from.errors), content_type='application/json')


class UserUploadView(LoginRequiredMixin, View):
    """
    用户头像上传
    """
    def post(self, request):
        image_from = UserUploadForm(request.POST, request.FILES, instance=request.user)
        if image_from.is_valid():
            # image = image_from.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_from.save()


class UpdateModifyPwdView(View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_forms = ResetForm(request.POST)
        if modify_forms.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                dict = {'status': 'fail', 'msg': '两次密码不一致'}
                return HttpResponse(json.dumps(dict), content_type='application/json')
            user = request.user
            user.password = make_password(password1)
            user.save()
            dict = {'status': 'success'}
            return HttpResponse(json.dumps(dict), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_forms.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            dict = {'status': 'fail', 'email': '邮箱已被注册'}
            return HttpResponse(json.dumps(dict), content_type='application/json')
        email_send(email, 'update_email')
        dict = {'status': 'success'}
        return HttpResponse(json.dumps(dict), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if UserProfile.objects.filter(email=email):
            dict = {'status': 'fail', 'email': '邮箱已被注册'}
            return HttpResponse(json.dumps(dict), content_type='application/json')
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            users = request.user
            users.email = email
            users.save()
            dict = {'status': 'success'}
            return HttpResponse(json.dumps(dict), content_type='application/json')
        else:
            dict = {'status': 'fail', 'msg': '验证码输入错误'}
            return HttpResponse(json.dumps(dict), content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-mycourse.html', {})


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        user_id = request.user.id
        my_orgs = UserFavorite.objects.filter(user_id=user_id, fav_type=2)
        for my_org in my_orgs:
            org = CourseOrg.objects.get(id=my_org.fav_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_tab': 'org'
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        user_id = request.user.id
        my_teachers = UserFavorite.objects.filter(user_id=user_id, fav_type=3)
        for my_teacher in my_teachers:
            org = Teacher.objects.get(id=my_teacher.fav_id)
            teacher_list.append(org)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_tab': 'teacher'
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        user_id = request.user.id
        my_courses = UserFavorite.objects.filter(user_id=user_id, fav_type=1)
        for my_course in my_courses:
            org = Course.objects.get(id=my_course.fav_id)
            course_list.append(org)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_tab': 'course'
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        print('user_id: ', request.user.id)
        all_message = UserMessage.objects.filter(user_id=request.user.id)
        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 3, request=request)
        messages = p.page(page)
        message_nums = all_message.count()
        return render(request, 'usercenter-message.html', {
            'messages': messages,
            'message_nums': message_nums
        })


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all()[:5]
        all_courses = Course.objects.filter(is_banner=1)[:3]
        all_course_banner = Course.objects.filter(is_banner=False)[:6]
        all_org = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner': all_banner,
            'all_courses': all_courses,
            'all_course_banner': all_course_banner,
            'all_org': all_org
        })




