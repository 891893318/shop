from django.core.mail import send_mail
from django.conf import settings

subject = "XXX邮箱验证"				# 标题
message = '尊敬的用户您好！.......' 	# 内容
to_email = '891893318@qq.com'		# 收件人

# settings.EMAIL_FROM 是发件人抬头, 收件人必须是列表,可多个收件人
send_mail(subject, message, settings.EMAIL_FROM, [to_email])  # 更多参数请查看源码
