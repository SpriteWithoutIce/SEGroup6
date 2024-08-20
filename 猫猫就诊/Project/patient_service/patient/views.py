import asyncio
from datetime import timedelta
import datetime
import os
from urllib.parse import quote, unquote
from django.utils import timezone
import re
from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.db.models import F, Q
from django.contrib.auth.hashers import check_password

import json

from patient_service import settings
from .models import *

from django.utils.deprecation import MiddlewareMixin
from doctor.models import OnDuty, Treatment
from administrator.models import Doctors
# Create your views here.

class MyCore(MiddlewareMixin):
    """
    处理HTTP响应，设置跨域请求的相关头部信息。
    Args:
        request: 请求对象，包含请求方法、请求头等信息。
        response: 响应对象，包含响应头、响应体等信息。
    Returns:
        修改后的响应对象，包含跨域请求相关的头部信息。
    """
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = '*'
        if request.method == 'OPTIONS':
            response["Access-Control-Allow-Headers"] = 'Content-Type'
            response["Access-Control-Allow-Methods"] = 'POST, DELETE, PUT'
        return response

class PatientView(APIView):
    """
    添加患者信息。
    Args:
        request (HttpRequest): 请求对象，包含请求体等属性。
    Returns:
        JsonResponse: 包含添加成功信息的JsonResponse对象。
    """
    def post(self, request):
        data = json.loads(request.body)
        patient = Patients.objects.filter(identity_num=data['number']).first()
        if patient is None:
            patient = Patients()
        if data['idType'] == '身份证':
            patient.identity = 1
        elif data['idType'] == '医保卡':
            patient.identity = 2
        elif data['idType'] == '诊疗卡':
            patient.identity = 3
        elif data['idType'] == '护照':
            patient.identity = 4
        elif data['idType'] == '军官证':
            patient.identity = 5
        elif data['idType'] == '港澳通行证':
            patient.identity = 6
        patient.identity_num = data['number']
        patient.name = data['name']
        if data['paymentType'] == '医保':
            patient.health_insurance = 1
        elif data['paymentType'] == '非医保':
            patient.health_insurance = 2
        if data['gender'] == '男':
            patient.gender = 1
        elif data['gender'] == '女':
            patient.gender = 2
        patient.birthday = data['birthday']
        patient.phone_num = data['phone']
        patient.address = data['addr']
        patient.save()
        return JsonResponse({'msg': 'Successfully add patient'})

class RegisterView(APIView):
    """
    处理POST请求，根据action参数执行相应的操作。
    Args:
        request: Django框架的HttpRequest对象，包含客户端发送的POST请求数据。
    Returns:
        JsonResponse: 返回JsonResponse对象，包含操作结果的数据。
    Raises:
        无。
    """
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getRegistersData':
            return self.getRegistersData(request)
        elif action == 'cancelRegister':
            return self.cancelRegister(request)
        elif action == 'getDoctorRegisters':
            return self.getDoctorRegisters(request)
        elif action == 'addRegisterData':
            return self.addRegisterData(request)
        elif action == 'lockRegister':
            return self.lockRegister(request)
        elif action == 'unlockRegister':
            return self.unlockRegister(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    """
    api/registers/list/
    根据传入的身份证号查询该医生的挂号信息，并返回JsonResponse格式数据
    Args:
        request: 包含挂号信息的请求对象
    Returns:
        包含挂号信息的JsonResponse格式数据
    Raises:
        无
    """
    def getRegistersData(self, request):
        identity_num = json.loads(request.body)['identity_num']
        registers = []
        filter = {}
        try:
            doctor = Doctors.objects.using('administrator_service').get(identity_num=identity_num)
            filter = {'doctor__identity_num': identity_num}
        except Doctors.DoesNotExist:
            filter = {'register': identity_num}
        for item in Register.objects.filter(**filter).exclude(queue_id=-1).annotate(
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
            doctor_name=F('doctor__name')
        ).values('id', 'queue_id', 'patient', 'patient_name', 'doctor_department',
                'doctor_name', 'time', 'position'):
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = item['time']
            end_time = start_time + timedelta(minutes=10)
            end_time = end_time.strftime('%H:%M')
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                formatted_datetime = formatted_datetime[:10] + ' '+ CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + ' '+ CHINESE_PM + formatted_datetime[10:]
            
            state = ""
            current_time = timezone.now()
            if start_time < current_time:
                state = "已就诊"
            else:
                state = "已预约"
            
            bill = Bill.objects.get(register=item['id'])
            registers.append({'id': item['id'],
                            'office': item['doctor_department'],
                            'orderNum': item['id'],
                            'price': bill.price,
                            'name': item['patient_name'],
                            'cardNum': item['patient'],
                            'position': item['position'],
                            'time': formatted_datetime + '-' + end_time,
                            'line': item['queue_id'],
                            'state': state,
                            'doctor': item['doctor_name']})
        return JsonResponse({'registers': registers})
    
    """
    api/registers/cancel/
    取消挂号
    Args:
        request: 请求对象，包含请求体
    Returns:
        JsonResponse: 返回JSON响应，包含取消挂号成功信息
    """
    def cancelRegister(self, request):
        id = json.loads(request.body)['id']
        register = Register.objects.get(id=id)
        bill = Bill.objects.get(register=id)
        time = 1
        if register.time.hour > 12:
            time = 2
        onDuty = OnDuty.objects.using('doctor_service').get(doctor=register.doctor, date=register.time.date(), time=time)
        onDuty.state = onDuty.state & (~(1 << (register.queue_id - 1)))
        onDuty.save()
        notice = Notice()
        notice.patient = register.patient
        notice.registerMan = register.register
        notice.doctor = register.doctor
        notice.msg_type = 2
        notice.time = timezone.now()
        notice.register = register
        notice.isRead = False
        notice.save()
        register.queue_id = -1
        register.save()
        bill.delete()
        return JsonResponse({'msg': "Successfully cancel register"})
    
    """
    api/registers/list/
    获取指定医生下的挂号记录
    Args:
        request: HttpRequest对象，请求对象
    Returns:
        JsonResponse对象，包含挂号记录的Json数据
    """
    def getDoctorRegisters(self, request):
        identity_num = json.loads(request.body)['identity_num']
        registers = []
        current_date = datetime.date.today()
        filter = {'doctor__identity_num': identity_num}
        for item in Register.objects.filter(**filter).exclude(queue_id=-1).annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('id', 'patient_name', 'patient_birthday', 'patient_gender', 'time'):
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (item['patient_birthday'].month, item['patient_birthday'].day))
            registers.append({
                "Id": item['id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": item['time'].date().strftime('%Y年%m月%d日')
            })
        return JsonResponse({'registers': registers})
    
    """
    api/appointment/add/
    新增挂号信息
    Args:
    - request: HTTP请求对象，包含请求体
    Returns:
    - JsonResponse: 包含成功信息的JsonResponse对象
    """
    def addRegisterData(self, request):
        data = json.loads(request.body)
        register = Register()
        register.queue_id = data['number']
        register.patient = Patients.objects.get(identity_num=data['inumber'])
        register.register = Patients.objects.get(identity_num=data['identity_num'])
        register.doctor = Doctors.objects.using('administrator_service').get(id=data['doctorId'])
        month, day = map(int, data['time'][:5].split('-'))
        hour, minute = map(int, data['starttime'].split(':'))
        register.time = timezone.now().replace(month=month, day=day, hour=hour, minute=minute)
        register.position = "猫猫医院" + data['department']
        register.save()
        bill = Bill()
        bill.type = 1
        bill.state = True
        bill.patient = register.patient
        bill.register = register
        bill.price = data['cost']
        bill.save()
        notice = Notice()
        notice.patient = register.patient
        notice.registerMan = register.register
        notice.doctor = register.doctor
        notice.msg_type = 1
        notice.time = timezone.now()
        notice.register = register
        notice.isRead = False
        notice.save()
        return JsonResponse({'msg': "Successfully add register"})
    
    """
    api/register/lock/
    锁定挂号
    Args:
        request (HttpRequest): 请求对象，包含请求体中的json数据
    Returns:
        JsonResponse: 包含锁定挂号结果的JsonResponse对象
    """
    def lockRegister(self, request):
        data = json.loads(request.body)
        queue_id = data['number']
        month, day = map(int, data['time'][:5].split('-'))
        hour, minute = map(int, data['starttime'].split(':'))
        startTime = timezone.now().replace(month=month, day=day, hour=hour, minute=minute)
        doctor = Doctors.objects.using('administrator_service').get(id=data['doctorId'])
        time = 1
        if startTime.hour > 12:
            time = 2
        onDuty = OnDuty.objects.using('doctor_service').get(doctor=doctor, date=startTime.date(), time=time)
        if (onDuty.state & (1 << (queue_id - 1))) != 0:
            return JsonResponse({"msg": "This register has been locked by others"})
        onDuty.state = onDuty.state | (1 << (queue_id - 1))
        onDuty.save()
        return JsonResponse({'msg': "Successfully lock register"})
    
    """
    api/register/unlock/
    解锁医生挂号
    Args:
        request: 请求对象，包含请求体body
    Returns:
        JsonResponse: 返回解锁挂号的结果，成功返回{"msg": "Successfully unlock register"}
    Raises:
        无
    """
    def unlockRegister(self, request):
        data = json.loads(request.body)
        queue_id = data['number']
        month, day = map(int, data['time'][:5].split('-'))
        hour, minute = map(int, data['starttime'].split(':'))
        startTime = timezone.now().replace(month=month, day=day, hour=hour, minute=minute)
        doctor = Doctors.objects.using('administrator_service').get(id=data['doctorId'])
        time = 1
        if startTime.hour > 12:
            time = 2
        onDuty = OnDuty.objects.using('doctor_service').get(doctor=doctor, date=startTime.date(), time=time)
        onDuty.state = onDuty.state & (~(1 << (queue_id - 1)))
        onDuty.save()
        return JsonResponse({'msg': "Successfully unlock register"})

class TreatmentView(APIView):
    """
    处理POST请求
    Args:
        request (HttpRequest): HTTP请求对象
    Returns:
        JsonResponse: JSON格式的响应对象
    Raises:
        无
    """
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getTreatmentsData':
            return self.getTreatmentsData(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    """
    api/treatments/list/
    获取治疗数据
    Args:
        request: 请求对象，需要包含identity_num字段
    Returns:
        JsonResponse: 包含治疗数据的JsonResponse对象
    """
    def getTreatmentsData(self, request):
        treatments = []
        identity_num = json.loads(request.body)['identity_num']
        filter = {}
        try:
            doctor = Doctors.objects.using('administrator_service').get(identity_num=identity_num)
            filter = {'doctor__identity_num': identity_num}
        except Doctors.DoesNotExist:
            filter = {'patient': identity_num}
        for item in Treatment.objects.using('doctor_service').filter(**filter).annotate(
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
            doctor_name=F('doctor__name')
        ).values('patient_name', 'doctor_department',
                'doctor_name', 'time', 'advice', 'medicine'):
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = item['time']
            end_time = start_time + timedelta(minutes=10)
            end_time = end_time.strftime('%H:%M')
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                formatted_datetime = formatted_datetime[:10] + ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + ' ' + CHINESE_PM + formatted_datetime[10:]
            treatments.append({'office': item['doctor_department'],
                            'time': formatted_datetime,
                            'patient': item['patient_name'],
                            'doctor': item['doctor_name'],
                            'advice': item['advice'],
                            'medicine': json.loads(item['medicine']),
            })
        return JsonResponse({'treatments': treatments})

class OnDutyView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        action = data['action']
        if action == 'getNextSevenDaysDuty':
            return self.getNextSevenDaysDuty(request)
        elif action == 'getAllNextSevenDaysDuty':
            return self.getAllNextSevenDaysDuty(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    # 返回一个科室接下来七天内所有医生值班情况
    def getNextSevenDaysDuty(self, request):
        duty = []
        seven_days_later = (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        department = json.loads(request.body)['department']
        for item in OnDuty.objects.using('doctor_service').filter(date__lte=seven_days_later, doctor__department=department).annotate(
            doctor_name=F('doctor__name'),
            doctor_title=F('doctor__title'),
            doctor_research=F('doctor__research'),
            doctor_avatar_name=F('doctor__avatar_name'),
            doctor_cost=F('doctor__cost')
        ).values('doctor_id', 'doctor_name', 'doctor_title', 'doctor_cost',
                'date', 'doctor_research', 'doctor_avatar_name', 'time', 'state'):
            time = ""
            if (item['time'] == 1):
                time = "(上午)"
            elif (item['time'] == 2):
                time = "(下午)"
            else:
                time = "(晚上)"
            rest = 0
            for i in range(20):
                if not (item['state'] & (1<<i)):
                    rest += 1
            find = False
            for d in duty:
                if d['id'] == item['doctor_id']:
                    emptyTime = []
                    for i in range(20):
                        emptyTime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                        })
                    d['schedule'].append({'time': item['date'].strftime('%m-%d') + time,
                                        'status': 'full' if rest == 0 else 'empty',
                                        'number': rest,
                                        "emptytime": emptyTime})
                    find = True
                    break
            if not find:
                emptyTime = []
                for i in range(20):
                    emptyTime.append({
                        "number": i + 1,
                        "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                    })
                duty.append({
                    "id": item['doctor_id'],
                    "name": item['doctor_name'],
                    "title": item['doctor_title'],
                    "research": item['doctor_research'],
                    "avatar": '/api/doctor/avatar/' + item['doctor_avatar_name'],
                    "cost": item['doctor_cost'],
                    "schedule": [{'time': item['date'].strftime('%m-%d') + time,
                                    'status': 'full' if rest == 0 else 'empty',
                                    'number': rest,
                                    "emptytime": emptyTime}],
                    
                })
        return JsonResponse({"duty": duty})
    
    def getAllNextSevenDaysDuty(self, request):
        duty = []
        seven_days_later = (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        for item in OnDuty.objects.using('doctor_service').filter(date__lte=seven_days_later).annotate(
            doctor_name=F('doctor__name'),
            doctor_title=F('doctor__title'),
            doctor_research=F('doctor__research'),
            doctor_department=F('doctor__department'),
            doctor_avatar_name=F('doctor__avatar_name'),
            doctor_cost=F('doctor__cost')
        ).values('doctor_id', 'doctor_name', 'doctor_title', 'doctor_department', 'doctor_cost',
                'date', 'doctor_research', 'doctor_avatar_name', 'time', 'state'):
            time = ""
            if (item['time'] == 1):
                time = "(上午)"
            elif (item['time'] == 2):
                time = "(下午)"
            else:
                time = "(晚上)"
            rest = 0
            for i in range(20):
                if not (item['state'] & (1<<i)):
                    rest += 1
            find = False
            for d in duty:
                if d['id'] == item['doctor_id']:
                    emptyTime = []
                    for i in range(20):
                        emptyTime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                        })
                    d['schedule'].append({'time': item['date'].strftime('%m-%d') + time,
                                        'status': 'full' if rest == 0 else 'empty',
                                        'number': rest,
                                        "emptytime": emptyTime})
                    find = True
                    break
            if not find:
                emptyTime = []
                for i in range(20):
                    emptyTime.append({
                        "number": i + 1,
                        "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                    })
                duty.append({
                    "id": item['doctor_id'],
                    "name": item['doctor_name'],
                    "title": item['doctor_title'],
                    "department": item['doctor_department'],
                    "research": item['doctor_research'],
                    "avatar": '/api/doctor/avatar/' + item['doctor_avatar_name'],
                    "schedule": [{'time': item['date'].strftime('%m-%d') + time,
                                    'status': 'full' if rest == 0 else 'empty',
                                    'number': rest,
                                    "emptytime": emptyTime}],
                    "cost": item['doctor_cost']
                })
        return JsonResponse({"duty": duty})

class BillView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getBillsData':
            return self.getBillsData(request)
        elif action == 'changeBillStatus':
            return self.changeBillStatus(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    def getBillsData(self, request):
        bill = []
        identity_num = json.loads(request.body)['identity_num']
        for item in Bill.objects.filter(patient=identity_num):
            department = item.register.doctor.department if item.type == 1 else item.treatment.doctor.department
            date = item.register.time.date() if item.type == 1 else item.treatment.time.date()
            bill.append({
                "id": item.id,
                "type": '挂号' if item.type == 1 else '处方',
                "department": department,
                "price": item.price,
                "date": date.strftime('%Y年%m月%d日'),
                "payStatus": item.state
            })
        return JsonResponse({"bill": bill})
    
    def changeBillStatus(self, request):
        data = json.loads(request.body)
        bill = Bill.objects.get(id=data['item_id'])
        bill.state = True
        bill.save()
        treatment = bill.treatment
        notice = Notice()
        notice.patient = treatment.patient
        notice.doctor = treatment.doctor
        notice.msg_type = 4
        notice.time = timezone.now()
        notice.treatment = treatment
        notice.isRead = False
        notice.save()
        return self.getBillsData(request)

class NoticeView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getMesData':
            return self.getNoticeData(request)
        elif action == 'readMes':
            return self.readNotice(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    def getNoticeData(self, request):
        resMes = []
        billMes = []
        identity_num = json.loads(request.body)['identity_num']
        for item in Notice.objects.filter(Q(patient=identity_num) | Q(registerMan=identity_num)).annotate(
            doctor_name=F('doctor__name'),
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
        ).values('id', 'patient', 'registerMan', 'msg_type', 'patient_name', 'doctor_name', 'doctor_department', 'treatment', 'register', 'time', 'isRead'):
            type = ""
            if item['msg_type'] == 1:
                type = "预约成功"
            elif item['msg_type'] == 2:
                type = "取消预约"
            elif item['msg_type'] == 3:
                type = "处方缴费提醒"
            else:
                type = "处方缴费成功"
            if (item['msg_type'] == 1 or item['msg_type'] == 2) and item['registerMan'] == identity_num:
                register = Register.objects.get(id=item['register'])
                resMes.append({
                    "item_id": item['id'],
                    "type": type,
                    "name": item['patient_name'],
                    "department": item['doctor_department'],
                    "doctor": item['doctor_name'],
                    "time": register.time.strftime('%Y-%m-%d %H:%M:%S'),
                    "id": item['patient'],
                    "timetamp": item['time'],
                    "read": item['isRead']
                })
            elif (item['msg_type'] == 3 or item['msg_type'] == 4) and item['patient'] == identity_num:
                treatment = Treatment.objects.using('doctor_service').get(id=item['treatment'])
                billMes.append({
                    "item_id": item['id'],
                    "type": type,
                    "name": item['patient_name'],
                    "department": item['doctor_department'],
                    "doctor": item['doctor_name'],
                    "time": item['time'].strftime('%Y-%m-%d %H:%M:%S'),
                    "id": item['patient'],
                    "timetamp": item['time'],
                    "price": treatment.price,
                    "read": item['isRead']
                })
        return JsonResponse({"resMes": resMes, "billMes": billMes})
    
    def readNotice(self, request):
        item_id = json.loads(request.body)['item_id']
        item = Notice.objects.get(id=item_id)
        item.isRead = True
        item.save()
        return JsonResponse({'msg': 'Successfully read'})