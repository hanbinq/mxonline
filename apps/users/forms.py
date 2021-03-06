# @Time : 2020/5/2 16:38 
# @Author : jing.liang
# @description :
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
     username = forms.CharField(required=True, min_length=2)
     password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
     mobile = forms.CharField(required=True, min_length=11, max_length=11)
     captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
     mobile = forms.CharField(required=True, min_length=11, max_length=11)
     code = forms.CharField(required=True, min_length=4, max_length=4)




