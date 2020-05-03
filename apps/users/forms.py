# @Time : 2020/5/2 16:38 
# @Author : jing.liang
# @description :
from django import forms


class LoginForm(forms.Form):
     username = forms.CharField(required=True, min_length=2)
     password = forms.CharField(required=True, min_length=3)



