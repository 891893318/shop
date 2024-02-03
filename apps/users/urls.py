"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path

from apps.users import views

apps_name = 'users'

urlpatterns = [
    # 注册
    path('register/', views.RegisterView.as_view(), name='register'),

    # 判断用户名是否重复
    # 写正则应该用re_path
    # 不用重定向，不需要写name
    # [\s\S\u4e00-\u9fa5]{2,20}$
    re_path(r'^usernames/(?P<username>[\s\S\u4e00-\u9fa5]{2,20})/count/$', views.UsernameCountView.as_view()),
    re_path(r'^emails/(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/count/$',
            views.EmailCountView.as_view()),
    path("login/", views.LogedInView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    # 个人中i性能
    path("user_info/", views.UserInfoView.as_view(), name='user_info'),
    # qq和微信登录
    path("QQAndWeixin/", views.QQAndWechatLoginView.as_view()),
    # 修改信息
    path("user_edit/<int:id>", views.ModifyInfoView.as_view())
]
