import asyncio
from datetime import timedelta
from datetime import datetime
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

from doctor_service import settings
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
        elif action == 'getDoctorRegisters':
            return self.getDoctorRegisters(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    """
    api/doctor_service/registers/list/
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
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/registers/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': filter, 'action': "filterRegister"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        registerList = response.json().get('registers', [])

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
    api/doctor_service/registers/list/
    获取指定医生下的挂号记录
    Args:
        request: HttpRequest对象，请求对象
    Returns:
        JsonResponse对象，包含挂号记录的Json数据
    """

    def getDoctorRegisters(self, request):
        identity_num = json.loads(request.body)['identity_num']
        registers = []
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        current_year, current_month, current_day = current_date.split('-')
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/exist/'
        # 请求数据（如果需要的话）
        requestData = {'identity_num': identity_num, 'action': "searchDoctor"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)

        filter = {'id': response.json().get('id')}
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/registers/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': filter, 'action': "filterRegister"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        registerList = response.json().get('registers', [])

        for item in registerList:
            birthday_year, birthday_month, birthday_day = item['patient_birthday'].split(
                '-')
            age = int(current_year) - int(birthday_year) - (int(current_month)
                                                            < int(birthday_month) or int(current_day) < int(birthday_day))
            year, month, day = item['time'].split('T')[0].split('-')
            registers.append({
                "Id": item['id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": f"{year}年{month}月{day}日"
            })
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
        elif action == 'addTreatmentData':
            return self.addTreatmentData(request)
        elif action == 'filterTreatment':
            return self.filterTreatment(request)
        elif action == 'searchTreatment':
            return self.searchTreatment(request)
        elif action == 'testAddTreatment':
            return self.testAddTreatment(request)
        elif action == 'getTreatment':
            return self.getTreatment(request)
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
        api_url = 'http://127.0.0.1:5003/api/administrator_service/doctors/list/'
        # 请求数据（如果需要的话）
        requestData = {'action': "getDoctorsData"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        doctorList = response.json().get('doctors', [])
        treatment = Treatment.objects.filter(**filter).first()

        for item in Treatment.objects.filter(doctor=filter['doctor']).values('patient', 'doctor', 'time', 'advice', 'medicine'):
            doctor = next(
                (doctor for doctor in doctorList if doctor['id'] == item['doctor']), None)
            doctor_department = doctor['department']
            doctor_name = doctor['name']
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            # print(type(item['time']))
            # start_time = datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
            start_time = item['time']
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_AM + formatted_datetime[10:]
            else:
                formatted_datetime = formatted_datetime[:10] + \
                    ' ' + CHINESE_PM + formatted_datetime[10:]
            patient_id = item['patient']
            # API 服务器地址
            api_url = 'http://127.0.0.1:5001/api/patient_service/patient/add/'
            requestData = {
                'number': patient_id,
                'action': "getPatientName"
            }
            patient_name = response.json().get('name')
            treatments.append({'office': doctor_department,
                               'time': formatted_datetime,
                               'patient': patient_name,
                               'doctor': doctor_name,
                               'advice': item['advice'],
                               'medicine': json.loads(item['medicine']),
                               })
        return JsonResponse({'treatments': treatments})

    """
    api/doctor_service/prescriptionDetailsWriteBack/
    添加治疗记录
    Args:
        request (HttpRequest): 包含治疗记录的请求体
    Returns:
        JsonResponse: 返回添加治疗记录的结果，成功时返回包含"msg"字段的JsonResponse，值为"Successfully add treatment"
    """

    def addTreatmentData(self, request):
        data = json.loads(request.body)
        if data['id'] < 0:
            return JsonResponse({'msg': "Invalid id"}, status=400)
        treatment = Treatment()
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/registers/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': {
            'id': data['id']}, 'action': "filterRegister"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        register = response.json()['registers'][0]
        treatment.queue_id = register['queue_id']
        treatment.patient = register['patient']
        treatment.doctor = register['doctor']
        treatment.time = timezone.now()
        treatment.advice = data['suggestion']
        treatment.medicine = json.dumps(data['medicines'])
        treatment.price = data['totalPrice']
        treatment.save()
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/add/bill/'
        # 请求数据（如果需要的话）

        requestData = {
            'type': 2,
            'state': "False",
            'patient': register['patient'],
            'treatment': treatment.id,
            'register': data['id'],
            'price': data['totalPrice'],
            'action': "addBill"}
        # 发送 POST 请求
        requests.post(api_url, json=requestData)
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/add/Notice/'
        # 请求数据（如果需要的话）
        requestData = {
            'patient': register['patient'],
            'registerMan': register['register'],
            'doctor': register['doctor'],
            'msg_type': 3,
            'time': '2024-08-20',
            'treatment': treatment.id,
            'isRead': "False",
            'action': "addNotice"}
        # 发送 POST 请求
        requests.post(api_url, json=requestData)
        return JsonResponse({'msg': "Successfully add treatment"})

    def filterTreatment(self, request):
        data = json.loads(request.body)
        treatments = []
        for item in Treatment.objects.filter(**data['filter']).values(
                'patient', 'time', 'doctor', 'advice', 'medicine'):
            treatments.append({'medicine': item['medicine'],
                               'doctor': item['doctor'],
                               'patient': item['patient'],
                               'time': item['time'],
                               'advice': item['advice']})
        return JsonResponse({'treatments': treatments})

    def searchTreatment(self, request):
        data = json.loads(request.body)
        try:
            treatment = Treatment.objects.get(id=data['id'])
            return JsonResponse({'msg': "Treatment Exist", 'price': treatment.price})
        except Treatment.DoesNotExist:
            return JsonResponse({'msg': "Treatment Not Exist"})

    def testAddTreatment(self, request):
        data = json.loads(request.body)
        if data['id'] < 0:
            return JsonResponse({'msg': "Invalid id"}, status=400)
        treatment = Treatment()
        # API 服务器地址
        api_url = 'http://127.0.0.1:5001/api/patient_service/registers/filter/'
        # 请求数据（如果需要的话）
        requestData = {'filter': {
            'id': data['id']}, 'action': "filterRegister"}
        # 发送 POST 请求
        response = requests.post(api_url, json=requestData)
        register = response.json()['registers'][0]
        treatment.queue_id = register['queue_id']
        treatment.patient = register['patient']
        treatment.doctor = register['doctor']
        treatment.time = timezone.now()
        treatment.advice = data['suggestion']
        treatment.medicine = json.dumps(data['medicines'])
        treatment.price = data['totalPrice']
        treatment.save()
        return JsonResponse({'msg': "Successfully add treatment", 'treatment_id': treatment.id})

    def getTreatment(self, request):
        data = json.loads(request.body)
        treatment = Treatment.objects.get(id=data['id'])
        treatments = []
        treatments.append({'id': treatment.id,
                           'queue_id': treatment.queue_id,
                           'patient': treatment.patient,
                           'doctor': treatment.doctor,
                           'time': treatment.time,
                           'advice': treatment.advice,
                           'medicine': treatment.medicine,
                           'price': treatment.price})
        return JsonResponse({'treatments': treatments})


class MedicineView(APIView):
    # api/doctor_service/medicine/list/
    def get(self, request):
        # API 服务器地址
        api_url = 'http://127.0.0.1:5003/api/administrator_service/medicine/list/'
        # 发送 POST 请求
        response = requests.get(api_url)
        medicineList = response.json().get('medicine', [])
        return JsonResponse({'medicine': medicineList})


class OnDutyView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'changeDutyState':
            return self.changeDutyState(request)
        elif action == 'judgeDutyState':
            return self.judgeDutyState(request)
        elif action == 'dutyListSevenDays':
            return self.dutyListSevenDays(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    def changeDutyState(self, request):
        data = json.loads(request.body)
        onDuty = OnDuty.objects.get(
            doctor=data['doctor'], date=data['date'], time=data['time'])
        onDuty.state = onDuty.state & (~(1 << (data['queue_id'] - 1)))
        onDuty.save()
        return JsonResponse({'msg': "Successfully change duty"})

    def judgeDutyState(self, request):
        data = json.loads(request.body)
        onDuty = OnDuty.objects.get(
            doctor=data['doctor'], date=data['date'], time=data['time'])
        if (onDuty.state & (1 << (data['queue_id'] - 1))) != 0:
            return JsonResponse({"msg": "This register has been locked by others"})
        onDuty.state = onDuty.state | (1 << (data['queue_id'] - 1))
        onDuty.save()
        return JsonResponse({'msg': "Successfully lock register"})

    def dutyListSevenDays(self, request):
        data = json.loads(request.body)
        onDutyList = []
        if 'department' in data:
            seven_days_later = (
                timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            for item in OnDuty.objects.filter(date__lte=seven_days_later).values(
                    'doctor', 'date', 'time', 'state'):
                # doctor=Doctors.objects.get(id=item['doctor'])
                api_url = "http://127.0.0.1:5003/api/administrator_service/doctors/getDoctor/"
                requestData = {
                    'identity_num': item['doctor'],
                    'id': item['doctor'],  # 医生编号
                    'action': 'getDoctor'
                }
                respond = requests.post(api_url, json=requestData)
                doctor = respond.json()['doctor'][0]
                if doctor['department'] == data['department']:
                    onDutyList.append({'doctor': item['doctor'],
                                       'date': item['date'],
                                       'time': item['time'],
                                       'state': item['state']})
            return JsonResponse({'onDutyList': onDutyList})
        else:
            seven_days_later = (
                timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            for item in OnDuty.objects.filter(date__lte=seven_days_later).values(
                    'doctor', 'date', 'time', 'state'):
                onDutyList.append({'doctor': item['doctor'],
                                   'date': item['date'],
                                   'time': item['time'],
                                   'state': item['state']})
            return JsonResponse({'onDutyList': onDutyList})
