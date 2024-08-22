from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from datetime import timedelta

from django.utils import timezone
from .models import *
import json
import requests

client = APIClient()


class TreatmentViewTest(APITestCase):
    def setUp(self):
        # 创建测试数据
        self.client = client
        api_url = 'http://127.0.0.1:5001/api/patient_service/patient/add/'
        requestData = {
            'name': "Existing Patient",
            'paymentType': "非医保",
            'gender': "男",
            'birthday': datetime.date.today().isoformat(),
            'idType': "身份证",
            'phone': "1234567890",
            'number': '123456',
            'addr': "Existing Address",
            'action': "getPatient"
        }
        self.patient = requests.post(
            api_url, json=requestData).json()['patients']

        api_url = 'http://127.0.0.1:5003/api/administrator_service/test/addDoctor/'
        # 请求数据（如果需要的话）
        requestData = {
            'identity_num': '1234567890',  # 证件号
            'name': '张三',                # 医生姓名
            'title': '主任医师',           # 医生职称
            'department': '内科',          # 医生科室
            'research': '心脏病研究',     # 研究方向，如果不需要可以省略或设置为None
            'cost': 200,                   # 出诊费，例如200元
            'avatar': 'path/to/avatar.jpg',  # 头像图片路径，如果不需要可以省略或设置为None
            'avatar_name': 'dr_zhang_san.jpg',  # 图片名字
            'action': 'testAddDoctor'
        }
        respond = requests.post(api_url, json=requestData)
        api_url = "http://127.0.0.1:5003/api/administrator_service/doctors/getDoctor/"
        requestData = {
            'identity_num': '1234567890',  # 证件号
            'action': 'getDoctor'
        }
        respond = requests.post(api_url, json=requestData)
        self.doctor = respond.json()['doctor']

        api_url = "http://127.0.0.1:5001/api/patient_service/appointment/add/"
        requestData = {
            'action': 'addRegisterData',
            'number': 1,
            'inumber': self.patient[0]['identity_num'],
            'identity_num': self.patient[0]['identity_num'],
            'doctorId': self.doctor[0]['id'],
            'time': "08-20-2024",
            'starttime': '09:00',
            'department': 'cat',
            'cost': 100
        }
        respond = requests.post(api_url, json=requestData)
        self.register_id = respond.json()['registers'][0]['id']
        self.data = {
            'action': 'getTreatmentsData',
            'identity_num': '1234567890'
        }
        requestData = {
            'action': 'addTreatmentData',
            'id': self.register_id,
            'suggestion': 'Take a rest',
            'medicines': ['Aspirin', 'Paracetamol'],
            'totalPrice': 100
        }
        url = reverse('treatment_list')
        self.client.post(url, requestData, format='json')

    def test_add_treatment_success(self):
        # 正向测试用例：成功添加治疗记录
        url = reverse('treatment_list')
        add_data = {
            'action': 'addTreatmentData',
            'id': self.register_id,
            'suggestion': 'Take a rest',
            'medicines': ['Aspirin', 'Paracetamol'],
            'totalPrice': 100
        }
        response = self.client.post(url, add_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'msg': 'Successfully add treatment'})

    def test_add_treatment_invalid_data(self):
        # 负向测试用例：使用无效数据添加治疗记录
        url = reverse('treatment_list')
        add_data = {
            'action': 'addTreatmentData',
            'id': -1,  # 无效的 register id
            'suggestion': '',
            'medicines': [],
            'totalPrice': 0
        }
        response = self.client.post(url, add_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_treatments_success(self):
        # 正向测试用例：成功获取治疗数据
        url = reverse('treatment_list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('treatments', response.json())


class OnDutyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        api_url = 'http://127.0.0.1:5003/api/administrator_service/test/addDoctor/'
        # 请求数据（如果需要的话）
        requestData = {
            'identity_num': '1234567890',  # 证件号
            'name': '张三',                # 医生姓名
            'title': '主任医师',           # 医生职称
            'department': '内科',          # 医生科室
            'research': '心脏病研究',     # 研究方向，如果不需要可以省略或设置为None
            'cost': 200,                   # 出诊费，例如200元
            'avatar': 'path/to/avatar.jpg',  # 头像图片路径，如果不需要可以省略或设置为None
            'avatar_name': 'dr_zhang_san.jpg',  # 图片名字
            'action': 'testAddDoctor'
        }
        requests.post(api_url, json=requestData)
        api_url = "http://127.0.0.1:5003/api/administrator_service/doctors/getDoctor/"
        requestData = {
            'identity_num': '1234567890',  # 证件号
            'action': 'getDoctor'
        }
        respond = requests.post(api_url, json=requestData)
        self.doctor = respond.json()['doctor'][0]

        self.on_duty = OnDuty.objects.create(
            doctor=self.doctor['id'],
            date=timezone.now() + timedelta(days=1),
            time=1,
            state=123
        )

    def test_get_next_seven_days_duty_successful(self):
        # 正向测试用例：成功的获取接下来七天的值班情况
        url = reverse('seven_days')
        response = self.client.post(url, {
            'action': 'dutyListSevenDays',
            'department': self.doctor['department']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_next_seven_days_duty_successful(self):
        # 正向测试用例：成功的获取所有接下来七天的值班情况
        url = reverse('seven_days')
        response = self.client.post(url, {
            'action': 'dutyListSevenDays'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
