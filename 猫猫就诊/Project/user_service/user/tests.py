from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import requests
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone
from .models import *
import json

client = APIClient()


class UserViewTest(APITestCase):
    def setUp(self):
        self.user_doctor = User.objects.create(
            identity_num='123456',
            password='password123',
            type=1
        )
        self.user_patient = User.objects.create(
            identity_num='654321',
            password='patientpass',
            type=2
        )
        api_url = 'http://127.0.0.1:5001/api/patient_service/patient/add/'
        requestData = {
            'name': "未填写",
            'paymentType': "非医保",
            'gender': "男",
            'birthday': datetime.date.today().isoformat(),
            'idType': "身份证",
            'phone': "未填写",
            'number': self.user_patient.identity_num,
            'addr': "未填写",
            'action': "getPatient"
        }
        requests.post(api_url, json=requestData)

    # 正向测试：测试成功登录
    def test_successful_login(self):
        url = reverse('user_login')
        data = {
            'idCard': '123456',
            'password': 'password123',
            'userType': '医生'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully Login'})

    # 负向测试：测试密码错误
    def test_failed_login_wrong_password(self):
        url = reverse('user_login')
        print(url)
        data = {
            'idCard': '123456',
            'password': 'wrongpassword',
            'userType': '医生'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Wrong Password'})

    # 负向测试：测试用户类型错误
    def test_failed_login_wrong_user_type(self):
        url = reverse('user_login')
        data = {
            'idCard': '123456',
            'password': 'password123',
            'userType': '普通用户'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Wrong Password'})

    # 正向测试：成功注册
    def test_successful_registration(self):
        url = reverse('user_login')
        data = {
            'idCard': '987654',
            'password': 'newpassword',
            'userType': '普通用户'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully Register'})
