from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone
from .models import *
import json
import requests

client = APIClient()


class TreatmentViewTest(APITestCase):
    def setUp(self):
        # 创建测试数据
        self.client = client
        api_url = 'http://127.0.0.1:8001/api/patient_service/patient/add/'
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
        respond = self.client.post(api_url, requestData, format='json')
        print(respond)
        self.patient = self.client.get(api_url, requestData, format='json')
        print(self.patient.status_code)
        exit()
        api_url = 'http://127.0.0.1:8002/api/administrator_service/doctors/addDoctor/'
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
        print(respond)
        # self.client.post(url, requestData, format='json')
        api_url = "http://127.0.0.1:8002/api/administrator_service/doctors/getDoctor/"
        requestData = {
            'identity_num': '1234567890',  # 证件号
            'action': 'getDoctor'
        }
        self.doctor = requests.post(api_url, json=requestData)
        print(self.doctor)
        # url = reverse('getDoctor')
        # self.doctor = self.client.post(url, requestData, format='json')

        self.data = {
            'action': 'getTreatmentsData',
            'identity_num': '1234567890'
        }

    def test_add_treatment_success(self):
        # 正向测试用例：成功添加治疗记录
        url = reverse('treatment_list')
        add_data = {
            'action': 'addTreatmentData',
            'id': '1234567890',
            'suggestion': 'Take a rest',
            'medicines': ['Aspirin', 'Paracetamol'],
            'totalPrice': 100
        }
        response = self.client.post(url, add_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'msg': 'Successfully add treatment'})

    # def test_add_treatment_invalid_data(self):
    #     # 负向测试用例：使用无效数据添加治疗记录
    #     url = reverse('treatment_list')
    #     add_data = {
    #         'action': 'addTreatmentData',
    #         'id': -1,  # 无效的 register id
    #         'suggestion': '',
    #         'medicines': [],
    #         'totalPrice': 0
    #     }
    #     response = self.client.post(url, add_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_treatments_success(self):
    #     # 正向测试用例：成功获取治疗数据
    #     url = reverse('treatment_list')
    #     response = self.client.post(url, self.data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('treatments', response.json())

    # def test_get_treatments_invalid_identity(self):
    #     # 负向测试用例：使用无效的 identity_num 获取治疗数据
    #     self.data['identity_num'] = 'invalid_identity'
    #     url = reverse('treatment_list')
    #     response = self.client.post(url, self.data, format='json')
    #     self.assertEqual(response.status_code,
    #                      status.HTTP_400_BAD_REQUEST)  # 状态码根据业务逻辑调整
    #     self.assertEqual(response.json(), {
    #                      'error': 'Invalid doctor'})


# class OnDutyViewTestCase(APITestCase):
#     def setUp(self):
#         # 设置测试数据
#         self.client = APIClient()
#         api_url = 'http://127.0.0.1:8002/api/administrator_service/doctors/setData/'
#         # 请求数据（如果需要的话）
#         requestData = {
#             'identity_num': '123456',  # 证件号
#             'name': 'John Doe',                # 医生姓名
#             'title': 'Dr.',           # 医生职称
#             'department': 'Cardiology',          # 医生科室
#             'research': 'Heart diseases',     # 研究方向，如果不需要可以省略或设置为None
#             'cost': 150,                   # 出诊费，例如200元
#             'avatar_name': 'avatar1.png',  # 图片名字
#             'action': 'testAddDoctor'
#         }
#         requests.post(api_url, json=requestData)
#         api_url = "http://127.0.0.1:8002/administrator_service/doctors/getDoctor/"
#         requestData = {
#             'identity_num': '123456',  # 证件号
#             'action': 'getDoctor'
#         }
#         self.doctor = requests.post(api_url, json=requestData)
#         self.on_duty = OnDuty.objects.create(
#             doctor=self.doctor,
#             date=timezone.now(),
#             time=1,
#             state=12
#         )

#     def test_get_next_seven_days_duty_successful(self):
#         # 正向测试用例：成功的获取接下来七天的值班情况
#         url = reverse('duty_next_seven_days')
#         response = self.client.post(url, {
#             'action': 'getNextSevenDaysDuty',
#             'department': self.doctor.department
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('duty', response.json())

#     def test_get_next_seven_days_duty_fault_no_department(self):
#         # 负向测试用例：缺少部门信息，导致获取失败
#         url = reverse('duty_next_seven_days')
#         response = self.client.post(url, {
#             'action': 'getNextSevenDaysDuty'
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json(), {
#                          'error': 'Missing "department" key'})

#     def test_get_all_next_seven_days_duty_successful(self):
#         # 正向测试用例：成功的获取所有接下来七天的值班情况
#         url = reverse('duty_all_next_seven_days')
#         response = self.client.post(url, {
#             'action': 'getAllNextSevenDaysDuty'
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('duty', response.json())

#     def test_get_all_next_seven_days_duty_fault_invalid_action(self):
#         # 负向测试用例：无效的操作导致失败
#         url = reverse('duty_all_next_seven_days')
#         response = self.client.post(url, {
#             'action': 'invalidAction'
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json(), {'error': 'Invalid action'})
