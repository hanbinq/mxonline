from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

import redis

from apps.users.forms import *
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from mxonline.settings import yunpian_apikey, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


class DynamicLoginView(View):
    def post(self, request):
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 没有注册账号依然可以使用
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {"login_form": login_form})


class SendSmsView(View):

    def post(self, request):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成数字验证码
            code = generate_random(4, 0)
            res_json = send_single_sms(yunpian_apikey, code, mobile=mobile)
            if res_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 5*60)
            else:
                re_dict["msg"] = res_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            "login_form": login_form,
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        # 表单验证
        if login_form.is_valid():
            # 用于通过用户和密码查询用户是否存在
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})

