from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django import forms
from django.utils.decorators import method_decorator
from django_redis import get_redis_connection
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, reverse
from django.views import View
from django import http

from . import models
from .forms import RegisterForm, LoginForm
from .models import User


# from users.models import User


class RegisterView(View):

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """提供用户注册逻辑"""
        # 校验参数
        register_form = RegisterForm(request.POST)
        # print("zhuce")

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            email = register_form.cleaned_data.get('email')
            email_code_client = register_form.cleaned_data.get('email_code')

            conn = get_redis_connection("verification")
            email_code_server = conn.get(f'email_{email}')
            print(email_code_server)

            if email_code_server is None:
                return render(request, 'register.html', {'email_code_errmsg': "验证码已失效"})
            if email_code_server.decode() != email_code_client:
                return render(request, 'register.html', {'email_code_errmsg': "验证码错误"})

            # 保存到数据库中
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
            except Exception as e:
                return render(request, 'register.html', {'register_errmsg': '注册失败！！！'})
            # print("123")
            # 状态保持
            login(request, user)
            # print("456")
            # 响应结果
            return redirect(reverse('contents:index'))
            # return redirect(reverse('contents:index'))
        else:
            print(register_form.errors.get_json_data())
            context = {
                'forms_errors': register_form.errors
            }
            return render(request, 'register.html', context=context)


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        """
        :param request:
        :param username:用户名
        :return:返回用户名是否重复 JSON
        """

        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})


class EmailCountView(View):
    """判断邮箱是否重复注册"""

    def get(self, request, email):
        """
        :param request:
        :param email:用户名
        :return:返回用户名是否重复 JSON
        """

        count = User.objects.filter(email=email).count()
        return http.JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})


class LogedInView(View):
    """用户登录逻辑"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data.get('username').encode('utf-8')
            password = login_form.cleaned_data.get('password')
            remembered = login_form.cleaned_data.get('remembered')
            print(username)

            if not all([username, password]):
                return http.HttpResponseForbidden("缺少参数")

            # user = User.objects.get(username=username)
            # pwd = user.password   # 数据库内密文
            #
            # if check_password(password, pwd):
            #     print("密码正确")
            # else:
            #     print("密码错误")
            user = authenticate(username=username.decode("utf-8"), password=password)
            if user is None:
                return render(request, 'login.html', {'account_errmsg': "账号或密码错误"})
            # 状态保持
            login(request, user)

            if not remembered:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            response = redirect(reverse('contents:index'))

            # 用户名写到cookie
            response.set_cookie('username', username)

            return response
        else:
            print(login_form.errors)
            context = {
                'forms_errors': login_form.errors
            }
            return render(request, 'login.html', context=context)


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """图吃登录"""
        # 强出状态保持
        logout(request)

        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')

        return response


class UserInfoView(View):
    """用户个人中心"""

    def get(self, request):
        """用户个人中心页面"""
        if request.user.is_authenticated:
            context = {
                'id': request.user.id,
                'username': request.user.username,
                'gender': request.user.get_gender_display(),
                'email': request.user.email,
                'name': request.user.name,
                'address': request.user.address,
            }
            return render(request, "user_center_info.html", context=context)
        else:
            return redirect("/users/login/")


class QQAndWechatLoginView(View):
    """qq和微信登陆"""

    def get(self, request):
        """
        :param request:
        :return:
        """
        return render(request, "A.html")


class UserModelForm(forms.ModelForm):
    class Meta:
        """不想全部都显示"""
        model = models.User
        fields = ["username", "name", "password", "gender", "address"]

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.NumberInput(attrs={"class": "form-control"}),
        #
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = ({"class": "form-control", "placeholder": field.label})


class ModifyInfoView(View):
    """
    def user_edit(request, id):

    obj = models.user.objects.filter(id=id).first()
    if request.method == "GET":
        form = UserModelForm(instance=obj)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/user_list/")
    else:
        return render(request, "user_edit.html", {"form": form})
    """

    @method_decorator(login_required)  # 登录保护
    def get(self, request, id):
        print("get")
        """提供用户修改信息页面"""
        # 获取当前用户信息
        user = request.user
        content = {
            "id": user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'gender': user.get_gender_display(),
            'address': user.address,
            'mobile': user.mobile
            # 添加其他需要修改的字段
        }
        print("get OVER")
        return render(request, 'user_edit.html', {'content': content})

    @method_decorator(login_required)  # 登录保护
    def post(self, request, id):
        print("post")
        """提供用户xiugai逻辑"""
        # 校验参数
        obj = models.User.objects.filter(id=id).first()

        form = UserModelForm(data=request.POST, instance=obj)
        print(form)
        # print("zhuce")

        if form.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')

            print("valid")
            hashed_password = make_password(password)

            # 保存到数据库中
            try:
                User.objects.filter(id=id).update(username=username, name=name, password=hashed_password, gender=gender,
                                                  address=address)
                print("try")
            except Exception as e:
                return render(request, 'user_edit.html', {'register_errmsg': '修改失败！！！'})

            # 响应结果
            return redirect('/users/user_info/')
            # return redirect(reverse('contents:index'))
        else:
            print("not_valid")
            context = {
                'forms_errors': "修改失败"
            }
            return render(request, 'user_edit.html', context=context)
