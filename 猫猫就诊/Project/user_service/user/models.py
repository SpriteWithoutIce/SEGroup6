import datetime
import django
from django.db import models

# Create your models here.

class User(models.Model):
    type_choices = (
        (1, "医生"),
        (2, "普通用户"),
        (3, "管理员"),
    )
    type = models.SmallIntegerField(verbose_name="用户类型", choices=type_choices, default=2)
    identity_num = models.CharField(verbose_name="证件号", max_length=64, primary_key=True)
    password = models.CharField(verbose_name="用户密码", max_length=64)