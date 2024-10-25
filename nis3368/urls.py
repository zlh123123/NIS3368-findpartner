"""
URL configuration for nis3368 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01 import views

urlpatterns = [
    path("", views.home),
    path("home/", views.home),
    path("login/", views.log),
    path("dashboard/", views.mainpage),
    path("main/", views.main),
    path("publish/",views.publish, name="publish"),
    path("my/",views.my),
    path("my/published/",views.published),
    path("my/replied/",views.replied),
    path("my/info/", views.info),
    path("message/",views.message),
    path("yinsixieyi/",views.yinsixieyi),
    path("kefu/",views.kefu),
    path("change_username/",views.change_username, name="change_username"),
    path("change_desc/",views.change_desc, name="change_desc"),
    path("change_avatar/",views.change_avatar, name="change_avatar"),
]
