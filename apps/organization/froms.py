#coding=utf-8
__author__ = 'kai.yang'
__date__ = '2019/9/8 22:14'

from django import forms
from opration.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        p = re.compile(r"^1[35678]\d{9}$")
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='this is not mobile')




