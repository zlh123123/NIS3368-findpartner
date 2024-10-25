import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from app01.function import *
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request: HttpRequest):
    request.session["is_login"] = False
    request.session["user_name"] = None
    return render(request, "home/home.html")

def log(request: HttpRequest):
    if request.session.get("is_login", None):
        return redirect("/dashboard/")
    
    if request.method == "GET" :
        return render(request, "home/login.html")

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data["log_username"]
            password = login_form.cleaned_data["log_password"]

            login_result = login(username, password)

            if login_result == 0:
                request.session["is_login"] = True
                request.session["user_name"] = username
                return redirect("/dashboard/")
            elif login_result == 1:
                messages.error(request, "密码错误！")
            elif login_result == -1:
                messages.error(request, "用户不存在！")

            return render(request, "home/login.html", locals())
        
        elif register_form.is_valid():
            username = register_form.cleaned_data["reg_username"]
            email = register_form.cleaned_data["reg_email"]
            password = register_form.cleaned_data["reg_password"]
            password2 = register_form.cleaned_data["reg_password2"]

            reg_result = register(username, password)

            if reg_result == 0:
                messages.success(request, "注册成功！")
                return redirect("/login/")
            elif reg_result == 1:
                messages.error(request, "用户已存在！")
            
            return render(request, "home/login.html", locals())

def mainpage(request):
    context = {
        "login_result": request.session.get("is_login", None),
    }
    return render(request, "mainpage/mainpage.html", context)

def main(request):
    return render(request, "mainpage/main.html")


def yinsixieyi(request):
    return render(request, "mainpage/yinsixieyi.html")


def kefu(request):
    return render(request, "mainpage/kefu.html")


def my(request):
    if request.method == "GET":
        if request.session.get("is_login", None):
            username = request.session["user_name"]
            user_info = check_user(username)
            if user_info.introduction == "unknown":
                user_info.introduction = "这个人还没有个人介绍"
            context = {
                "user_name": username,
                "user_introduction": user_info.introduction,
                "user_avatar": user_info.image,
                "user_id": user_info.id,
            }
            return render(request, "user/my.html", context)
        else:
            messages.error(request, "请先登录！")
            return redirect("/login/")

def change_username(request):
    if request.method == "POST":
        new_username = request.POST.get("username")
        username = request.session["user_name"]
        if new_username == username:
            messages.error(request, "新用户名不能与旧用户名相同！")
            return redirect("/my/")
        
        if not re.match(r'^[a-zA-Z0-9]{6,18}$', new_username):
            messages.error(request, "用户名必须为6-18位字母或数字！")
            return redirect("/my/")
        
        user_info = check_user(username)
        user_info.user_name = new_username
        result = change_user_info(username,user_info) 
        if result == 0:
            messages.success(request, "修改成功！")
            request.session["user_name"] = new_username
            return redirect("/my/")
        else:
            messages.error(request, "修改失败！")
            return redirect("/my/")
        
    return render(request, "user/myoptions/mychangeinfo.html")


def change_desc(request):
    if request.method == "POST":
        new_desc = request.POST.get("desc")
        username = request.session["user_name"]

        if new_desc == "":
            messages.error(request, "个人介绍不能为空！")
            return redirect("/my/")
        
        user_info = check_user(username)
        user_info.introduction = new_desc
        result = change_user_info(username,user_info)

        if result == 0:
            messages.success(request, "修改成功！")
            return redirect("/my/")
        else:
            messages.error(request, "修改失败！")
            return redirect("/my/")
        
    return render(request, "user/myoptions/mychangeinfo.html")

def change_avatar(request):
    if request.method == "POST":
        image_url = request.POST.get("image_url")
        username = request.session["user_name"]
        
        if image_url == "":
            messages.error(request, "请先上传图片！")
            return redirect("/my/")

        user_info = check_user(username)
        user_info.image = image_url
        result = change_user_info(username,user_info)

        if result == 0:
            messages.success(request, "修改成功！")
            return redirect("/my/")
        else:
            messages.error(request, "修改失败！")
            return redirect("/my/")
        
    return render(request, "user/myoptions/mychangeinfo.html")

def published(request):
    return render(request, "user/myoptions/mypublished.html")

@csrf_exempt   
def publish(request):

    if not request.session.get("is_login", None):
        return redirect("/dashboard/")  # 如果未登录，重定向到仪表盘

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            title = data.get('title', "unknown")  # 默认值为"unknown"
            contact = data.get('contact')
            content = data.get('content')
            category = data.get('category', 0)  # 默认值为0
            tags = data.get('tags') if data.get('tags') else []  # 确保 tags 是一个列表
            image_url = data.get('imageUrl')
            current_date = data.get('date', "unknown")  # 默认值为"unknown"

            notice_id = add_notice(
                request.session["user_name"]
            )  # 传入当前用户名或用户ID
            #print(notice_id)
            if notice_id == -1:
                return JsonResponse({'error': '用户不存在'}, status=400)

            notice = check_notice(notice_id)
            if notice is None:
                return JsonResponse({'error': '获取通知失败'}, status=400)

            notice.owner_contact = contact
            notice.title = title
            notice.basic_type = category
            notice.image = image_url
            notice.time = current_date
            notice.description = content
            notice.tag_list = tags 

            if change_notice(notice) == -1:
                return JsonResponse({'error': '更新通知失败'}, status=400)

            return JsonResponse({'message': '发布成功'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '发布失败，数据格式错误'}, status=400)

    return render(request, "user/push.html")


def replied(request):
    return render(request, "user/myoptions/myreplied.html")

def info(request):
    return render(request, "user/myoptions/mychangeinfo.html")
def message(request):
    return render(request, "user/message.html")
