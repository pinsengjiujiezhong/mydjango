#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/8/29 22:59'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    '''
    max_length:  最大的长度
    min_length： 最小的长度
    required： 是否必填  True为必填项
    '''
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForGetPwdForm(forms.Form):
    email = forms.EmailField(required=True, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True, max_length=15)
    password2 = forms.CharField(required=True, max_length=15)


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']