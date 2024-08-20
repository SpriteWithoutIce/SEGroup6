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

class Doctors(models.Model):
    identity_num = models.CharField(verbose_name="证件号", max_length=64)
    name = models.CharField(verbose_name="医生姓名", max_length=20)
    title = models.CharField(verbose_name="医生职称", max_length=50)
    department = models.CharField(verbose_name="医生科室", max_length=20)
    research = models.CharField(verbose_name="研究方向", max_length=150, null=True, blank=True)
    cost = models.DecimalField(verbose_name="出诊费", max_digits=5, decimal_places=2)
    avatar = models.ImageField(verbose_name="医生头像", upload_to='doctor/', null=True, blank=True)
    avatar_name = models.CharField(verbose_name="图片名字", max_length=128, default="img")

class OnDuty(models.Model):
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="值班日期", default=django.utils.timezone.now)
    time_choices = (
        (1, "上午"),
        (2, "下午"),
        (3, "晚上"),
    )
    time = models.SmallIntegerField(verbose_name="值班时间", choices=time_choices, default=1)
    state = models.IntegerField(verbose_name="预约状态")

class Register(models.Model):
    queue_id = models.IntegerField(verbose_name="排队号", default=1)
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='patient_registers')
    register = models.ForeignKey(verbose_name="挂号者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='register_registers')
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="挂号时间")
    position = models.CharField(verbose_name="门诊位置", max_length=128)

class Treatment(models.Model):
    queue_id = models.IntegerField(verbose_name="排队号", default=1)
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE)
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="就诊时间")
    advice = models.CharField(verbose_name="诊断结果", max_length=256)
    medicine = models.TextField(verbose_name="开具药物")
    price = models.DecimalField(verbose_name="处方总价", max_digits=5, decimal_places=2)

class Bill(models.Model):
    type_choices = (
        (1, "挂号"),
        (2, "处方"),
    )
    type = models.SmallIntegerField(verbose_name="账单类型", choices=type_choices)
    
    state = models.BooleanField(verbose_name="账单状态")
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, null=True, blank=True)
    treatment = models.ForeignKey(verbose_name="处方编号", to="Treatment", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(verbose_name="挂号编号", to="Register", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(verbose_name="账单金额", max_digits=5, decimal_places=2)

class Notice(models.Model):
    patient = models.ForeignKey(verbose_name="患者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='patient_notices')
    registerMan = models.ForeignKey(verbose_name="挂号者证件号", to="Patients", to_field="identity_num", on_delete=models.CASCADE, related_name='register_notices', null=True, blank=True)
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    
    type_choices1 = (
        (1, "预约成功"),
        (2, "取消预约"),
        (3, "处方缴费提醒"),
        (4, "处方缴费成功"),
    )
    msg_type = models.SmallIntegerField(verbose_name="消息类型", choices=type_choices1)
    time = models.DateTimeField(verbose_name="通知时间")
    treatment = models.ForeignKey(verbose_name="处方编号", to="Treatment", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(verbose_name="挂号编号", to="Register", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    isRead = models.BooleanField(verbose_name="已读未读", default=False)

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