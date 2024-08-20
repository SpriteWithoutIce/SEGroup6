import datetime
import django
from django.db import models
# Create your models here.

class OnDuty(models.Model):
    doctor = models.IntegerField(verbose_name="医生编号")
    date = models.DateField(verbose_name="值班日期", default=django.utils.timezone.now)
    time_choices = (
        (1, "上午"),
        (2, "下午"),
        (3, "晚上"),
    )
    time = models.SmallIntegerField(verbose_name="值班时间", choices=time_choices, default=1)
    state = models.IntegerField(verbose_name="预约状态")

class Treatment(models.Model):
    queue_id = models.IntegerField(verbose_name="排队号", default=1)
    patient = models.IntegerField(verbose_name="患者证件号")
    doctor = models.IntegerField(verbose_name="医生编号")
    time = models.DateTimeField(verbose_name="就诊时间")
    advice = models.CharField(verbose_name="诊断结果", max_length=256)
    medicine = models.TextField(verbose_name="开具药物")
    price = models.DecimalField(verbose_name="处方总价", max_digits=5, decimal_places=2)