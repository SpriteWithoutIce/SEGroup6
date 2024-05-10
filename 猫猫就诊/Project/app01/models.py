import datetime
from django.db import models

# Create your models here.
class Users(models.Model):
    account = models.CharField(verbose_name="用户账号", max_length=32, primary_key=True)
    password = models.CharField(verbose_name="用户密码", max_length=64)
    
    type_choices = (
        (1, "患者"),
        (2, "医生"),
        (3, "管理员"),
    )
    user_type = models.SmallIntegerField(verbose_name="用户类型", choices=type_choices)

class Patients(models.Model):
    account = models.ForeignKey(verbose_name="患者账号", to="Users", to_field="account", on_delete=models.CASCADE)
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
    
    birthday = models.DateField(verbose_name="患者生日", default=datetime.date.today)
    phone_num = models.CharField(verbose_name="患者电话", max_length=15, default="")
    
    identity_choices = (
        (1, "身份证"),
        (2, "医保卡"),
        (3, "诊疗卡"),
        (4, "护照"),
        (5, "军官证"),
        (6, "港澳通行证"),
    )
    identity = models.SmallIntegerField(verbose_name="身份证明", choices=identity_choices, default=1)
    identity_num = models.CharField(verbose_name="证件号", max_length=64, default="")
    address = models.CharField(verbose_name="患者住址", max_length=128, default="")

class Doctors(models.Model):
    account = models.ForeignKey(verbose_name="医生账号", to="Users", to_field="account", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="医生姓名", max_length=20)
    
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    title = models.CharField(verbose_name="医生职称", max_length=50)
    section = models.CharField(verbose_name="医生科室", max_length=20)
    research = models.CharField(verbose_name="研究方向", max_length=150, null=True, blank=True)

class OnDuty(models.Model):
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", primary_key=True, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="值班日期", default=datetime.date.today)
    
    time_choices = (
        (1, "上午"),
        (2, "下午"),
        (3, "晚上"),
    )
    time = models.SmallIntegerField(verbose_name="值班时间", choices=time_choices, default=1)
    
    state = models.IntegerField(verbose_name="预约状态")

class Register(models.Model):
    patient = models.ForeignKey(verbose_name="患者编号", to="Patients", to_field="id", on_delete=models.CASCADE)
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="挂号时间")

class Treatment(models.Model):
    patient = models.ForeignKey(verbose_name="患者编号", to="Patients", to_field="id", on_delete=models.CASCADE)
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="就诊时间")
    medicine = models.CharField(verbose_name="处方内容", max_length=200)
    
    state_choices = (
        (1, "已缴费"),
        (2, "待缴费"),
    )
    state = models.SmallIntegerField(verbose_name="处方状态", choices=state_choices)

class Notice(models.Model):
    patient = models.ForeignKey(verbose_name="患者编号", to="Patients", to_field="id", on_delete=models.CASCADE)
    message = models.CharField(verbose_name="通知内容", max_length=200)

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