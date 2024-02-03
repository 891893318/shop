from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=32, unique=True, verbose_name="邮箱", null=True, default='xxxxxx@email.com')
    name = models.CharField(max_length=32, unique=True, verbose_name="真实姓名", null=True, default='')
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号", null=True, default='')
    address = models.CharField(max_length=512, verbose_name="住址", null=True, default='')

    # 追加字段
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, default=1)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
