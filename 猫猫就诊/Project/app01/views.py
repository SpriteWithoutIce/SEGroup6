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

from backend import settings
from .models import *

from django.utils.deprecation import MiddlewareMixin
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


class UserView(APIView):
    """
    处理用户登录和注册请求
    Args:
        request: HTTP请求对象，包含请求头和请求体
    Returns:
        JsonResponse: JSON格式的响应对象，包含以下键值对：
            - msg: 字符串类型，表示操作结果，可选值为'Successfully Login'、'Wrong Password'、'Successfully Register'
    """

    def post(self, request):
        data = json.loads(request.body)
        identity_num = data["idCard"]
        pwd = data["password"]
        type = data['userType']
        if type == "医生":
            type = 1
        elif type == "普通用户":
            type = 2
        else:
            type = 3
        try:
            user = User.objects.get(identity_num=identity_num)
            if pwd == user.password and type == user.type:
                return JsonResponse({'msg': 'Successfully Login'})
            else:
                return JsonResponse({'msg': 'Wrong Password'})
        except User.DoesNotExist:
            user = User(
                identity_num=identity_num,
                password=pwd,
                type=type,
            )
            user.save()
            patient = Patients.objects.filter(
                identity_num=identity_num).first()
            if patient is None:
                patient = Patients()
                patient.identity = 1
                patient.identity_num = identity_num
                patient.name = "未填写"
                patient.health_insurance = 1
                patient.gender = 1
                patient.birthday = datetime.date.today()
                patient.phone_num = "未填写"
                patient.address = "未填写"
                patient.save()
            return JsonResponse({'msg': 'Successfully Register'})


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
        else:
            return JsonResponse({'msg': 'Error: Patient with this ID already exists.'})
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
            doctor = Doctors.objects.get(identity_num=identity_num)
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
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_PM + formatted_datetime[10:]

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
    取消挂号
    Args:
        request: 请求对象，包含请求体
    Returns:
        JsonResponse: 返回JSON响应，包含取消挂号成功信息
    """

    def cancelRegister(self, request):
        id = json.loads(request.body)['id']
        # modify
        register = Register.objects.filter(id=id).first()
        if register is None:
            return JsonResponse({'error': 'No such register'}, status=400)
        bill = Bill.objects.get(register=id)
        time = 1
        if register.time.hour > 12:
            time = 2
        onDuty = OnDuty.objects.get(
            doctor=register.doctor, date=register.time.date(), time=time)
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
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (
                item['patient_birthday'].month, item['patient_birthday'].day))
            registers.append({
                "Id": item['id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": item['time'].date().strftime('%Y年%m月%d日')
            })
        return JsonResponse({'registers': registers})

    """
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
        # modify
        if register.queue_id < 0:
            return JsonResponse({'msg': "No such queue"})
        register.patient = Patients.objects.get(identity_num=data['inumber'])
        register.register = Patients.objects.get(
            identity_num=data['identity_num'])
        register.doctor = Doctors.objects.get(id=data['doctorId'])
        month, day = map(int, data['time'][:5].split('-'))
        hour, minute = map(int, data['starttime'].split(':'))
        register.time = timezone.now().replace(
            month=month, day=day, hour=hour, minute=minute)
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
        doctor = Doctors.objects.get(id=data['doctorId'])
        time = 1
        if startTime.hour > 12:
            time = 2
        onDuty = OnDuty.objects.get(
            doctor=doctor, date=startTime.date(), time=time)
        if (onDuty.state & (1 << (queue_id - 1))) != 0:
            return JsonResponse({"msg": "This register has been locked by others"})
        onDuty.state = onDuty.state | (1 << (queue_id - 1))
        onDuty.save()
        return JsonResponse({'msg': "Successfully lock register"})

    """
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
        doctor = Doctors.objects.get(id=data['doctorId'])
        time = 1
        if startTime.hour > 12:
            time = 2
        onDuty = OnDuty.objects.get(
            doctor=doctor, date=startTime.date(), time=time)
        onDuty.state = onDuty.state & (~(1 << (queue_id - 1)))
        onDuty.save()
        return JsonResponse({'msg': "Successfully unlock register"})


class TreatmentView(APIView):
    """
    获取就诊列表信息
    Args:
        request: Django请求对象
    Returns:
        JsonResponse: 包含预约信息的Json响应对象
    Returns的JsonResponse格式:
        {
            "treatments": [
                {
                    "Id": int,             # 预约ID
                    "name": str,           # 患者姓名
                    "age": int,            # 患者年龄
                    "sex": str,            # 患者性别
                    "date": str            # 预约日期，格式为'%Y年%m月%d日'
                },
                ...
            ]
        }
    """

    def get(self, request):
        treatments = []
        current_date = datetime.date.today()
        for item in Treatment.objects.annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('queue_id', 'patient_name', 'patient_birthday', 'patient_gender', 'time'):
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (
                item['patient_birthday'].month, item['patient_birthday'].day))
            year, month, day, hour, minute = map(
                int, item['time'].split('-') + item['time'].split()[1].split(':'))
            date = datetime(year, month, day, hour, minute).date()
            treatments.append({
                "Id": item['queue_id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": item['time'].date().strftime('%Y年%m月%d日')
            })
        return JsonResponse({'treatments': treatments})

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
        elif action == 'addTreatmentData':
            return self.addTreatmentData(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    """
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
            # modify
            doctor = Doctors.objects.filter(identity_num=identity_num).first()
            if doctor is None:
                return JsonResponse({'error': 'Invalid doctor'}, status=400)
            filter = {'doctor__identity_num': identity_num}
        except Doctors.DoesNotExist:
            filter = {'patient': identity_num}
        for item in Treatment.objects.filter(**filter).annotate(
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
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_PM + formatted_datetime[10:]
            treatments.append({'office': item['doctor_department'],
                               'time': formatted_datetime,
                               'patient': item['patient_name'],
                               'doctor': item['doctor_name'],
                               'advice': item['advice'],
                               'medicine': json.loads(item['medicine']),
                               })
        return JsonResponse({'treatments': treatments})

    """
    添加治疗记录
    Args:
        request (HttpRequest): 包含治疗记录的请求体
    Returns:
        JsonResponse: 返回添加治疗记录的结果，成功时返回包含"msg"字段的JsonResponse，值为"Successfully add treatment"
    """

    def addTreatmentData(self, request):
        data = json.loads(request.body)
        treatment = Treatment()
        # modify
        register = Register.objects.filter(id=data['id']).first()
        if register is None:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        # register = Register.objects.get(id=data['id'])
        treatment.queue_id = register.queue_id
        treatment.patient = register.patient
        treatment.doctor = register.doctor
        treatment.time = timezone.now()
        treatment.advice = data['suggestion']
        treatment.medicine = json.dumps(data['medicines'])
        treatment.price = data['totalPrice']
        treatment.save()
        bill = Bill()
        bill.type = 2
        bill.state = False
        bill.patient = register.patient
        bill.treatment = treatment
        bill.price = data['totalPrice']
        bill.save()
        notice = Notice()
        notice.patient = register.patient
        notice.registerMan = register.register
        notice.doctor = register.doctor
        notice.msg_type = 3
        notice.time = timezone.now()
        notice.treatment = treatment
        notice.isRead = False
        notice.save()
        return JsonResponse({'msg': "Successfully add treatment"})


class DoctorView(APIView):
    """
    获取医生列表
    Args:
        request: HTTP请求对象
    Returns:
        JsonResponse: 返回一个包含医生信息的JsonResponse对象
    """

    def get(self, request):
        doctors = []
        for item in Doctors.objects.values('identity_num', 'name', 'department',
                                           'title', 'research', 'cost', 'avatar_name'):
            doctors.append({
                'id': item['identity_num'],
                'name': item['name'],
                'office': item['department'],
                'title': item['title'],
                'research': item['research'],
                'cost': item['cost'],
                'avatar_name': item['avatar_name']
            })
        # modify
        return JsonResponse({'doctors': doctors}, status=200)

    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'upload_avatar':
            return self.upload_avatar(request)
        elif action == 'getDoctorsData':
            return self.getDoctorsData(request)
        elif action == 'deleteDoctor':
            return self.deleteDoctor(request)
        elif action == 'removeAvatar':
            return self.removeAvatar(request)
        elif action == 'addDoctor':
            return self.addDoctor(request)
        elif action == 'alterDoctor':
            return self.alterDoctor(request)
        else:
            # mofify
            return JsonResponse({'error': 'Invalid action'})

    # 上传医生头像, 返回该医生数据
    def upload_avatar(self, request):
        doctor = Doctors.objects.get(account=request.POST.get("account"))
        doctor.avatar = request.FILES.get('avatar')
        doctor.save()
        return JsonResponse({"doctor": doctor})

    def getDoctorsData(self, request):
        doctors = []
        for item in Doctors.objects.values('id', 'name', 'department', 'title', 'research', 'avatar_name'):
            doctors.append({
                'id': item['id'],
                'name': item['name'],
                'department': item['department'],
                'title': item['title'],
                'research': item['research'],
                'avatar': '/api/doctor/avatar/' + item['avatar_name']
            })
        return JsonResponse({'doctors': doctors})

    def deleteDoctor(self, request):
        id = json.loads(request.body)['id']
        # modify
        doctor = Doctors.objects.filter(identity_num=id).first()
        if doctor is None:
            return JsonResponse({'msg': "Doctor with id {} not found".format(id)}, status=400)
        Doctors.objects.get(identity_num=id).delete()
        return self.get(request)

    def removeAvatar(self, request):
        avatar_name = json.loads(request.body)['avatar_name']
        file_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, avatar_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return JsonResponse({'msg': "Successfully removed avatar"})

    def addDoctor(self, request):
        data = json.loads(request.body)
        try:
            # modify
            doctor = Doctors.objects.filter(identity_num=data['id']).first()
            if doctor is not None:
                return JsonResponse({'msg': "Doctor with id {} already exists".format(id)}, status=400)
            doctor = Doctors()
            doctor.name = data['name']
            doctor.title = data['title']
            doctor.department = data['department']
            doctor.cost = data['cost']
            doctor.identity_num = data['id']
            doctor.research = data['research']
            doctor.avatar_name = data['avatar_name']
            doctor.save()
            # modify
            return JsonResponse({'msg': "Successfully add doctor data"}, status=200)
        except Doctors.DoesNotExist:
            return JsonResponse({'msg': "Doctor with id {} not found".format(id)}, status=404)

    def alterDoctor(self, request):
        data = json.loads(request.body)
        try:
            doctor = Doctors.objects.get(identity_num=data['id'])
            doctor.name = data['name']
            doctor.title = data['title']
            doctor.department = data['department']
            doctor.cost = data['cost']
            doctor.identity_num = data['id']
            doctor.research = data['research']
            doctor.avatar_name = data['avatar_name']
            doctor.save()
            return JsonResponse({'msg': "Successfully altered doctor data"})
        except Medicine.DoesNotExist:
            return JsonResponse({'msg': "Doctor with id {} not found".format(id)}, status=404)


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
        seven_days_later = (
            timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        # modify
        data = json.loads(request.body)
        if 'department' not in data:
            return JsonResponse({'error': 'Missing "department" key'}, status=400)
        department = json.loads(request.body)['department']
        for item in OnDuty.objects.filter(date__lte=seven_days_later, doctor__department=department).annotate(
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
                if not (item['state'] & (1 << i)):
                    rest += 1
            find = False
            for d in duty:
                if d['id'] == item['doctor_id']:
                    emptyTime = []
                    for i in range(20):
                        emptyTime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1 << i)) else 'full',
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
                        "status": "empty" if not (item['state'] & (1 << i)) else 'full',
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
        # modify
        return JsonResponse({"duty": duty}, status=200)

    def getAllNextSevenDaysDuty(self, request):
        duty = []
        seven_days_later = (
            timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        for item in OnDuty.objects.filter(date__lte=seven_days_later).annotate(
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
                if not (item['state'] & (1 << i)):
                    rest += 1
            find = False
            for d in duty:
                if d['id'] == item['doctor_id']:
                    emptyTime = []
                    for i in range(20):
                        emptyTime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1 << i)) else 'full',
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
                        "status": "empty" if not (item['state'] & (1 << i)) else 'full',
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
        # modify
        data = json.loads(request.body)
        if 'identity_num' not in data:
            return JsonResponse({'error': 'Invalid id'}, status=400)
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
        # modify
        if data['item_id'] < 0:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        bill = Bill.objects.filter(id=data['item_id']).first()
        # bill = Bill.objects.get(id=data['item_id'])
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
        data = json.loads(request.body)
        # modify
        if 'identity_num' not in data:
            return JsonResponse({'error': 'Missing identity number'}, status=400)
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
                treatment = Treatment.objects.get(id=item['treatment'])
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
        # modify
        return JsonResponse({"resMes": resMes, "billMes": billMes}, status=200)

    def readNotice(self, request):
        item_id = json.loads(request.body)['item_id']
        # modify
        if item_id < 0:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        item = Notice.objects.get(id=item_id)
        item.isRead = True
        item.save()
        # modify
        return JsonResponse({'msg': 'Successfully read'}, status=200)


class MedicineView(APIView):
    def get(self, request):
        medicine = []
        for item in Medicine.objects.values('id', 'name', 'medicine_type', 'symptom', 'price', 'quantity', 'photo_name'):
            type = ""
            if item['medicine_type'] == 1:
                type = "中药"
            elif item['medicine_type'] == 2:
                type = "中成药"
            else:
                type = "西药"
            medicine.append({
                'id': item['id'],
                "name": item['name'],
                "type": type,
                "use": item['symptom'],
                "price": item['price'],
                "num": item['quantity'],
                "photo_name": item['photo_name'],
            })
        return JsonResponse({'medicine': medicine})

    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'deleteMedicine':
            return self.deleteMedicine(request)
        elif action == 'removePhoto':
            return self.removePhoto(request)
        elif action == 'addMedicine':
            return self.addMedicine(request)
        elif action == 'alterMedicine':
            return self.alterMedicine(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def deleteMedicine(self, request):
        id = json.loads(request.body)['id']
        # modify
        medicine = Medicine.objects.filter(id=id).first()
        if medicine is None:
            return JsonResponse({'error': 'Medicine with id {} not found'.format(id)}, status=400)
        Medicine.objects.get(id=id).delete()
        return self.get(request)

    def removePhoto(self, request):
        photo_name = json.loads(request.body)['photo_name']
        file_path = os.path.join(settings.MEDICINE_PHOTO_ROOT, photo_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return JsonResponse({'msg': "Successfully removed photo"})

    def addMedicine(self, request):
        data = json.loads(request.body)
        try:
            # modify
            if 'name' not in data or 'type' not in data or 'symptom' not in data or 'price' not in data or 'quantity' not in data or 'photo_name' not in data:
                return JsonResponse({'error': 'Invalid data'}, status=400)
            medicine = Medicine()
            medicine.name = data['name']
            medicine.medicine_type = data['type']
            medicine.symptom = data['symptom']
            medicine.price = data['price']
            medicine.quantity = data['quantity']
            medicine.photo_name = data['photo_name']
            medicine.save()
            return JsonResponse({'msg': "Successfully add medicine data"})
        except Medicine.DoesNotExist:
            return JsonResponse({'msg': "Medicine with id {} not found".format(id)}, status=404)

    def alterMedicine(self, request):
        data = json.loads(request.body)
        try:
            medicine = Medicine.objects.get(id=data['id'])
            medicine.name = data['name']
            medicine.medicine_type = data['type']
            medicine.symptom = data['symptom']
            medicine.price = data['price']
            medicine.quantity = data['quantity']
            medicine.photo_name = data['photo_name']
            medicine.save()
            return JsonResponse({'msg': "Successfully altered medicine data"})
        except Medicine.DoesNotExist:
            return JsonResponse({'msg': "Medicine with id {} not found".format(id)}, status=404)


class UploadPhotoView(APIView):
    def get(self, request, filename, *args, **kwargs):
        photo_path = os.path.join(settings.MEDICINE_PHOTO_ROOT, filename)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as f:
                # 根据实际图片类型调整 content_type
                return HttpResponse(f.read(), content_type='image/jpeg')
        else:
            raise Http404("Photo not found")

    def post(self, request):
        file = request.FILES.get('file')
        file_path = os.path.join(settings.MEDICINE_PHOTO_ROOT, file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb+') as f:
            f.write(file.read())
        url = '/api/medicine/photo/' + file.name
        return JsonResponse({'msg': "Successfully uploaded photo", 'name': file.name, 'url': url})


class UploadAvatarView(APIView):
    def get(self, request, filename, *args, **kwargs):
        photo_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, filename)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as f:
                # 根据实际图片类型调整 content_type
                return HttpResponse(f.read(), content_type='image/jpeg')
        else:
            raise Http404("Photo not found")

    def post(self, request):
        file = request.FILES.get('file')
        file_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb+') as f:
            f.write(file.read())
        url = '/api/doctor/avatar/' + file.name
        return JsonResponse({'msg': "Successfully uploaded photo", 'name': file.name, 'url': url})
