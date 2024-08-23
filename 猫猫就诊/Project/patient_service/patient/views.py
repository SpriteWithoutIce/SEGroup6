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
import requests
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
        if 'action' in data and data['action'] == 'getPatient':
            return self.getPatient(request)
        if 'action' in data and data['action'] == 'getPatientName':
            return self.getPatientName(request)
        patient = Patients.objects.filter(identity_num=data['number']).first()
        if patient is None:
            patient = Patients()
        else:
            return JsonResponse({'msg': 'Patient already exists'}, status=400)
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
        patient.birthday = datetime.date.fromisoformat(data['birthday'])
        patient.phone_num = data['phone']
        patient.address = data['addr']
        patient.save()
        return JsonResponse({'msg': 'Successfully add patient'}, status=200)

    def getPatient(self, request):
        data = json.loads(request.body)
        patient = Patients.objects.get(identity_num=data['number'])
        patient_respond = []
        patient_respond.append({
            'id': patient.pk,
            'identity_num': patient.identity_num,
            'name': patient.name,
            'health_insurance': patient.get_health_insurance_display(),
            'gender': patient.get_gender_display(),
            'birthday': str(patient.birthday),
            'phone_num': patient.phone_num,
            'address': patient.address
        })
        return JsonResponse({'patients': patient_respond}, status=200)

    def getPatientName(self, request):
        data = json.loads(request.body)
        patient = Patients.objects.get(identity_num=data['number'])
        return JsonResponse({'name': patient.name}, status=200)


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
        elif action == 'filterRegister':
            return self.filterRegister(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    """
    api/patient_service/registers/list/
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
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/exist/'
        # 请求数据（如果需要的话）
        requestData = {'identity_num': identity_num, 'action': "searchDoctor"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)

        if response.json().get('msg') == "Doctor Exist":
            filter = {'doctor': response.json().get('id')}
        else:
            filter = {'register': identity_num}
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/registers/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': filter, 'action': "filterRegister"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        registerList = response.json().get('registers', [])
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        for item in registerList:
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            doctor_department = doctor['department']
            doctor_name = doctor['name']
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = item['time'].replace('T', ' ').split('.')[0]

            formatted_datetime = start_time
            hour = start_time[12:14]
            if hour < "12":
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_PM + formatted_datetime[10:]

            state = ""
            current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            date_time_parts1 = [
                int(part) for part in start_time.split(' ', 1)[1].split(':')]
            date_time_parts2 = [
                int(part) for part in current_time.split(' ', 1)[1].split(':')]
            if date_time_parts1 < date_time_parts2:
                state = "已就诊"
            else:
                state = "已预约"

            hour, minute, second = start_time.split(' ', 1)[1].split(':')
            hour = int(hour)
            minute = int(minute)
            minute += 10
            if minute >= 60:
                hour += 1
                minute -= 60
            end_time = f"{hour:02d}:{minute:02d}"

            # API 服务器地址
            api_url = 'http://127.0.0.1:5001/api/patient_service/bills/register/'
            # 请求数据（如果需要的话）
            requestData = {'register': item['id'], 'action': "registerBill"}
            # 发送 POST 请求
            response = requests.post(api_url, json=requestData)

            # 请求数据（如果需要的话）'})
            bill = response.json().get('bill')

            registers.append({'id': item['id'],
                              'office': doctor_department,
                              'orderNum': item['id'],
                              'price': bill['price'],
                              'name': item['patient_name'],
                              'cardNum': item['patient'],
                              'position': item['position'],
                              'time': formatted_datetime + '-' + end_time,
                              'line': item['queue_id'],
                              'state': state,
                              'doctor': doctor_name})
        return JsonResponse({'registers': registers})

    """
    api/patient_service/registers/cancel/
    取消挂号
    Args:
        request: 请求对象，包含请求体
    Returns:
        JsonResponse: 返回JSON响应，包含取消挂号成功信息
    """

    def cancelRegister(self, request):
        id = json.loads(request.body)['id']
        register = Register.objects.filter(id=id).first()
        if register is None:
            return JsonResponse({'error': 'No such register'}, status=400)
        bill = Bill.objects.get(register=id)
        time = 1
        if register.time.hour > 12:
            time = 2
        # API 服务器地址
        api_url = '/api/doctor_service/changeDutyState/'
        # 请求数据（如果需要的话）
        requestData = {'doctor': register.doctor,
                       'date': register.time.date(),
                       'time': time,
                       'queue_id': register.queue_id,
                       'action': "changeDutyState"}
        # 发送 POST 请求
        requests.post(api_url, json=requestData)
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
    api/patient_service/registers/list/
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
        # API 服务器地址
        api_url = '/api/administrator_service/doctors/exist/'
        # 请求数据（如果需要的话）
        requestData = {'identity_num': identity_num, 'action': "searchDoctor"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        filter = {'doctor': response.json().get('id')}
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
    api/patient_service/appointment/add/
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
        if register.queue_id < 0:
            return JsonResponse({'msg': "No such queue"})
        register.patient = Patients.objects.get(identity_num=data['inumber'])
        register.register = Patients.objects.get(
            identity_num=data['identity_num'])
        register.doctor = data['doctorId']
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
        registers = []
        registers.append({
            'id': register.id
        })
        return JsonResponse({'msg': "Successfully add register", 'registers': registers})

    """
    api/patient_service/register/lock/
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
        time = 1
        if startTime.hour > 12:
            time = 2
        api_url = '/api/doctor_service/judgeDutyState/'
        # 请求数据（如果需要的话）
        requestData = {'doctor': data['doctorId'],
                       'date': startTime.date(),
                       'time': time,
                       'queue_id': queue_id,
                       'action': "judgeDutyState"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        return JsonResponse(response.json())

    """
    api/patient_service/register/unlock/
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
        time = 1
        if startTime.hour > 12:
            time = 2
        # API 服务器地址
        api_url = '/api/doctor_service/changeDutyState/'
        # 请求数据（如果需要的话）
        requestData = {'doctor': data['doctorId'],
                       'date': startTime.date(),
                       'time': time,
                       'queue_id': queue_id,
                       'action': "changeDutyState"}
        # 发送 POST 请求
        requests.post(api_url, json=requestData)
        return JsonResponse({'msg': "Successfully unlock register"})

    def filterRegister(self, request):
        data = json.loads(request.body)
        registers = []
        for item in Register.objects.filter(**data['filter']).exclude(queue_id=-1).annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('id', 'queue_id', 'register', 'patient', 'patient_name',
                 'patient_birthday', 'patient_gender', 'doctor', 'time', 'position'):
            registers.append({'id': item['id'],
                              'queue_id': item['queue_id'],
                              'register': item['register'],
                              'patient': item['patient'],
                              'patient_name': item['patient_name'],
                              'patient_birthday': item['patient_birthday'],
                              'patient_gender': item['patient_gender'],
                              'doctor': item['doctor'],
                              'time': item['time'],
                              'position': item['position']})
        return JsonResponse({'registers': registers})


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
    api/patient_service/treatments/list/
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
        # API 服务器地址
        api_url = '/api/administrator_service/doctors/exist/'
        # 请求数据（如果需要的话）
        requestData = {'identity_num': identity_num, 'action': "searchDoctor"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        if response.json().get('msg') == "Doctor Exist":
            filter = {'doctor': response.json().get('id')}
        else:
            filter = {'patient': identity_num}
        # API 服务器地址
        api_url = '/api/doctor_service/treatments/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': filter, 'action': "filterTreatment"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        treatmentList = response.json().get('treatments', [])
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        for item in treatmentList:
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            doctor_department = doctor['department']
            doctor_name = doctor['name']
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
            end_time = start_time + timedelta(minutes=10)
            end_time = end_time.strftime('%H:%M')
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_PM + formatted_datetime[10:]
            treatments.append({'office': doctor_department,
                               'time': formatted_datetime,
                               'patient': Patients.objects.get(identity_num=item['patient']).name,
                               'doctor': doctor_name,
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
        data = json.loads(request.body)
        if 'department' not in data:
            return JsonResponse({'error': 'Missing "department" key'}, status=400)
        department = json.loads(request.body)['department']
        # API 服务器地址
        api_url = '/api/doctor_service/duty_list/seven_days'
        # 请求数据（如果需要的话）
        requestData = {'action': "dutyListSevenDays"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        onDutyList = response.json().get('onDutyList', [])
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        for item in onDutyList:
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            if doctor['department'] != department:
                continue
            doctor_name = doctor['name']
            doctor_title = doctor['title']
            doctor_research = doctor['research']
            doctor_avatar_name = doctor['avatar_name']
            doctor_cost = doctor['cost']
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
                if d['id'] == item['doctor']:
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
                    "id": item['doctor'],
                    "name": doctor_name,
                    "title": doctor_title,
                    "research": doctor_research,
                    "avatar": '/api/administrator_service/doctor/avatar/' + doctor_avatar_name,
                    "cost": doctor_cost,
                    "schedule": [{'time': item['date'].strftime('%m-%d') + time,
                                  'status': 'full' if rest == 0 else 'empty',
                                  'number': rest,
                                  "emptytime": emptyTime}],

                })
        return JsonResponse({"duty": duty}, status=200)

    def getAllNextSevenDaysDuty(self, request):
        duty = []
        # API 服务器地址
        api_url = '/api/doctor_service/duty_list/seven_days'
        # 请求数据（如果需要的话）
        requestData = {'action': "dutyListSevenDays"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        onDutyList = response.json().get('onDutyList', [])
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        for item in onDutyList:
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            doctor_department = doctor['department']
            doctor_name = doctor['name']
            doctor_title = doctor['title']
            doctor_research = doctor['research']
            doctor_avatar_name = doctor['avatar_name']
            doctor_cost = doctor['cost']
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
                if d['id'] == item['doctor']:
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
                    "id": item['doctor'],
                    "name": doctor_name,
                    "title": doctor_title,
                    "department": doctor_department,
                    "research": doctor_research,
                    "avatar": '/api/administrator_service/doctor/avatar/' + doctor_avatar_name,
                    "schedule": [{'time': item['date'].strftime('%m-%d') + time,
                                  'status': 'full' if rest == 0 else 'empty',
                                  'number': rest,
                                  "emptytime": emptyTime}],
                    "cost": doctor_cost
                })
        return JsonResponse({"duty": duty})


class BillView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getBillsData':
            return self.getBillsData(request)
        elif action == 'changeBillStatus':
            return self.changeBillStatus(request)
        elif action == 'registerBill':
            return self.registerBill(request)
        elif action == 'addBill':
            return self.addBill(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def getBillsData(self, request):
        bills = []
        data = json.loads(request.body)
        if 'identity_num' not in data:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        identity_num = json.loads(request.body)['identity_num']
        bill = Bill.objects.all()
        for item in bill:
            patient_id = item.patient
            if patient_id is None:
                continue

            if item.patient != identity_num:
                continue
            patient = Patients.objects.get(identity_num=patient_id)
            if item.type == 1:
                register = item.register
                api_url = "http://127.0.0.1:5003/api/administrator_service/doctors/getDoctor/"
                requestData = {
                    'identity_num': register.doctor,
                    'action': 'getDoctor'
                }
                respond = requests.post(api_url, json=requestData)
                doctor = respond.json()['doctor'][0]
                department = doctor['department']
                date = item.register.time.date()
            else:
                treatment = item.treatment
                api_url = "http://127.0.0.1:5003/api/administrator_service/doctors/getDoctor/"
                requestData = {
                    'id': treatment.doctor,  # 证件号
                    'action': 'getDoctor'
                }
                respond = requests.post(api_url, json=requestData)
                doctor = respond.json()['doctor'][0]
                department = doctor['department']
                date = item.treatment.time.date()
            bills.append({
                "id": item.id,
                "type": '挂号' if item.type == 1 else '处方',
                "department": department,
                "price": item.price,
                "date": date.strftime('%Y年%m月%d日'),
                "payStatus": item.state
            })
            return JsonResponse({"bill": bills}, status=200)
        return JsonResponse({"bill": bills}, status=200)
        # for item in Bill.objects.filter(patient__identity_num=identity_num):
        #     department = item.register.doctor.department if item.type == 1 else item.treatment.doctor.department
        #     return JsonResponse({'department': department})
        #     date = item.register.time.date() if item.type == 1 else item.treatment.time.date()
        #     bill.append({
        #         "id": item.id,
        #         "type": '挂号' if item.type == 1 else '处方',
        #         "department": department,
        #         "price": item.price,
        #         "date": date.strftime('%Y年%m月%d日'),
        #         "payStatus": str(item.state)
        #     })
        # return JsonResponse({"bill": bill})

    def changeBillStatus(self, request):
        data = json.loads(request.body)
        if data['item_id'] < 0:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        bill = Bill.objects.get(id=data['item_id'])
        bill.state = True
        bill.save()
        api_url = "http://127.0.0.1:5002/api/doctor_service/treatments/list/"
        requestData = {
            'id': bill.treatment,
            'action': 'getTreatment'
        }
        respond = requests.post(api_url, json=requestData)
        treatment = respond.json()['treatments'][0]
        notice = Notice()
        notice.patient = Patients.objects.get(
            identity_num=treatment['patient'])
        notice.doctor = treatment['doctor']
        notice.msg_type = 4
        notice.time = timezone.now()
        notice.treatment = bill.treatment
        notice.isRead = False
        notice.save()
        return self.getBillsData(request)

    def registerBill(self, request):
        data = json.loads(request.body)
        bill = Bill.objects.all()
        for item in bill:
            register = item.register
            if register is None:
                continue
            if register.id == data['register']:
                bill_data = {'price': item.price}
                break
        return JsonResponse({'bill': bill_data})
        return JsonResponse({'id': register.doctor})
        bill = Bill.objects.get(register=register).value('price')
        bill_data = {'price': bill['price']}
        return JsonResponse({'bill': bill_data})

    def addBill(self, request):
        data = json.loads(request.body)
        bill = Bill()
        bill.type = data['type']
        bill.state = data['state']
        bill.patient = Patients.objects.get(identity_num=data['patient'])
        bill.treatment = data['treatment']
        bill.register = Register.objects.get(id=data['register'])
        bill.price = data['price']
        bill.save()


class NoticeView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getMesData':
            return self.getNoticeData(request)
        elif action == 'readMes':
            return self.readNotice(request)
        elif action == 'addNotice':
            return self.addNotice(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def getNoticeData(self, request):
        resMes = []
        billMes = []
        data = json.loads(request.body)
        if 'identity_num' not in data:
            return JsonResponse({'error': 'Missing identity number'}, status=400)
        identity_num = json.loads(request.body)['identity_num']
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        for item in Notice.objects.filter(Q(patient=identity_num) | Q(registerMan=identity_num)).annotate(
            patient_name=F('patient__name'),
        ).values('id', 'patient', 'doctor', 'registerMan', 'msg_type', 'patient_name', 'treatment', 'register', 'time', 'isRead'):
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            doctor_name = doctor['name']
            doctor_department = doctor['department']
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
                    "department": doctor_department,
                    "doctor": doctor_name,
                    "time": register.time.strftime('%Y-%m-%d %H:%M:%S'),
                    "id": item['patient'],
                    "timetamp": item['time'],
                    "read": item['isRead']
                })
            elif (item['msg_type'] == 3 or item['msg_type'] == 4) and item['patient'] == identity_num:
                # API 服务器地址
                api_url = '/api/treatment/exist/'
                # 请求数据（如果需要的话）
                requestData = {'id': item['treatment'],
                               'action': "searchTreatment"}
                # 发送 POST 请求
                response = requests.post(api_url, json=requestData)
                price = response.json().get('price', None)
                billMes.append({
                    "item_id": item['id'],
                    "type": type,
                    "name": item['patient_name'],
                    "department": doctor_department,
                    "doctor": doctor_name,
                    "time": item['time'].strftime('%Y-%m-%d %H:%M:%S'),
                    "id": item['patient'],
                    "timetamp": item['time'],
                    "price": price,
                    "read": item['isRead']
                })
        return JsonResponse({"resMes": resMes, "billMes": billMes}, status=200)

    def readNotice(self, request):
        item_id = json.loads(request.body)['item_id']
        if item_id < 0:
            return JsonResponse({'error': 'Invalid id'}, status=400)
        item = Notice.objects.get(id=item_id)
        item.isRead = True
        item.save()
        return JsonResponse({'msg': 'Successfully read'}, status=200)

    def addNotice(self, request):
        data = json.loads(request.body)
        notice = Notice()
        notice.patient = Patients.objects.get(identity_num=data['patient'])
        notice.registerMan = Patients.objects.get(
            identity_num=data['registerMan'])
        notice.doctor = data['doctor']
        notice.msg_type = data['msg_type']
        notice.time = data['time']
        notice.treatment = data['treatment']
        notice.isRead = data['isRead']
        notice.save()
