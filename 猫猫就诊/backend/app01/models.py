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

class Doctors(models.Model):
    account = models.ForeignKey(verbose_name="医生账号", to="Users", to_field="account", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="医生姓名", max_length=20)
    title = models.CharField(verbose_name="医生职称", max_length=50)
    section = models.CharField(verbose_name="医生科室", max_length=20)
    speciality = models.CharField(verbose_name="医生特长", max_length=150)

class OnDuty(models.Model):
    doctor = models.ForeignKey(verbose_name="医生编号", to="Doctors", to_field="id", primary_key=True, on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name="开始时间")
    end = models.DateTimeField(verbose_name="结束时间")
    
    state_choices = (
        (1, "已预约"),
        (2, "空闲"),
    )
    state = models.SmallIntegerField(verbose_name="预约状态", choices=state_choices)

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