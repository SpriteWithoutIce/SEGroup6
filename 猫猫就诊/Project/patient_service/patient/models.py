import datetime
import django
from django.db import models

# Create your models here.

class Patients(models.Model):
    identity_choices = (
        (1, "身份证"),
        (2, "医保卡"),
        (3, "诊疗卡"),
        (4, "护照"),
        (5, "军官证"),
        (6, "港澳通行证"),
    )
    identity = models.SmallIntegerField(verbose_name="身份证明", choices=identity_choices, default=1)
    identity_num = models.CharField(verbose_name="证件号", max_length=64, primary_key=True)
    name = models.CharField(verbose_name="患者姓名", max_length=20)
    health_insurance_choices = (
        (1, "医保"),
        (2, "非医保"),
    )
    health_insurance = models.SmallIntegerField(verbose_name="医保情况", choices=health_insurance_choices, default=1)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="患者性别", choices=gender_choices)
    birthday = models.DateField(verbose_name="患者生日", default=django.utils.timezone.now)
    phone_num = models.CharField(verbose_name="患者电话", max_length=15, default="")
    address = models.CharField(verbose_name="患者住址", max_length=128, default="")



class Register(models.Model):
    queue_id = models.IntegerField(verbose_name="排队号", default=1)
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='patient_registers')
    register = models.ForeignKey(verbose_name="挂号者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='register_registers')
    doctor = models.IntegerField(verbose_name="医生编号")
    time = models.DateTimeField(verbose_name="挂号时间")
    position = models.CharField(verbose_name="门诊位置", max_length=128)

class Bill(models.Model):
    type_choices = (
        (1, "挂号"),
        (2, "处方"),
    )
    type = models.SmallIntegerField(verbose_name="账单类型", choices=type_choices)
    
    state = models.BooleanField(verbose_name="账单状态")
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, null=True, blank=True)
    treatment = models.IntegerField(verbose_name="处方编号", null=True, blank=True)
    register = models.ForeignKey(verbose_name="挂号编号", to="Register", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(verbose_name="账单金额", max_digits=5, decimal_places=2)

class Notice(models.Model):
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='patient_notices')
    registerMan = models.ForeignKey(verbose_name="挂号者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='register_notices', null=True, blank=True)
    doctor = models.IntegerField(verbose_name="医生编号")
    
    type_choices1 = (
        (1, "预约成功"),
        (2, "取消预约"),
        (3, "处方缴费提醒"),
        (4, "处方缴费成功"),
    )
    msg_type = models.SmallIntegerField(verbose_name="消息类型", choices=type_choices1)
    time = models.DateTimeField(verbose_name="通知时间")
    treatment = models.IntegerField(verbose_name="处方编号", null=True, blank=True)
    register = models.ForeignKey(verbose_name="挂号编号", to="Register", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    isRead = models.BooleanField(verbose_name="已读未读", default=False)