import datetime
import django
from django.db import models

# Create your models here.

class Doctors(models.Model):
    identity_num = models.CharField(verbose_name="证件号", max_length=64)
    name = models.CharField(verbose_name="医生姓名", max_length=20)
    title = models.CharField(verbose_name="医生职称", max_length=50)
    department = models.CharField(verbose_name="医生科室", max_length=20)
    research = models.CharField(verbose_name="研究方向", max_length=150, null=True, blank=True)
    cost = models.DecimalField(verbose_name="出诊费", max_digits=5, decimal_places=2)
    avatar = models.ImageField(verbose_name="医生头像", upload_to='doctor/', null=True, blank=True)
    avatar_name = models.CharField(verbose_name="图片名字", max_length=128, default="img")

class Medicine(models.Model):
    name = models.CharField(verbose_name="药物名字", max_length=50)
    medicine_choices = (
        (1, "中药"),
        (2, "中成药"),
        (3, "西药"),
    )
    medicine_type = models.SmallIntegerField(verbose_name="药物种类", choices=medicine_choices)
    symptom = models.CharField(verbose_name="适应症状", max_length=200)
    price = models.DecimalField(verbose_name="药物价格", max_digits=5, decimal_places=2)
    quantity = models.IntegerField(verbose_name="药物库存", default=0)
    photo_name = models.CharField(verbose_name="图片名字", max_length=128, default="img")