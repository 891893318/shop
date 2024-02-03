import random
# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText

from django import http
from django.core import mail
from django.core.mail import send_mail
from django.views import View
from django_redis import get_redis_connection


from utils.response_code import RETCODE
from .constants import *


# class ImageCodeView(View):
#     """图形验证码"""
#
#     def get(self, request, uuid):
#         """
#         :param request:
#         :param uuid: 通用唯一识别符,用于标识唯一图片验证码属于哪个用户的
#         :return: image/jpg
#         """
#
#         # 生成图片验证码
#         text, image = captcha.generate_captcha()
#         # print(text, image)
#
#         # 保存图像验证码,保存到redis
#         redis_conn = get_redis_connection('verification')
#
#         # name time value
#         redis_conn.setex(f'img_code{uuid}', IMAGE_CODE_REDIS_EXPIRES, text)
#
#         # 响应图形验证码
#         return http.HttpResponse(image, content_type='image/png')


class CodeView(View):
    """短信验证码"""

    def get(self, request, email):
        """
        :param request:
        :param email: 手机号
        :return: JSON
        """

        redis_conn = get_redis_connection('verification')

        # 生成短信验证码
        # 生成6位的随机数  %6d
        email_code = "%06d" % random.randint(0, 999999)

        # 保存短信验证码
        redis_conn.setex(f'email_{email}', EMAIL_CODE_REDIS_EXPIRES, email_code)

        # 发送
        # 邮件内容
        mail.send_mail(
            subject='验证码',  # 题目
            message=email_code,  # 消息内容
            from_email='730347390@qq.com',  # 发送者[当前配置邮箱]
            recipient_list=[email],  # 接收者邮件列表
        )
        # send_email_code.delay(email_code, email)

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送验证码成功'})
