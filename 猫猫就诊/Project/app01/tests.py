from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import User, Patients

client = APIClient()


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(type=2, identity_num='22373443', password='1234')

    def test_user_creation(self):
        user = User.objects.get(identity_num='22373443')
        self.assertEqual(user.password, '1234')


class UserViewTest(APITestCase):
    def setUp(self):
        # 创建测试用的User和Patients数据
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
        self.patient = Patients.objects.create(
            identity_num='654321',
            name="Test_Patient",
            health_insurance=1,
            gender=1,
            birthday=date.today(),
            phone_num="1234567890",
            address="Test Address"
        )

    def test_successful_login(self):
        # 测试成功登录
        url = reverse('user_login')
        data = {
            'idCard': '123456',
            'password': 'password123',
            'userType': '医生'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully Login'})

    def test_failed_login_wrong_password(self):
        # 测试密码错误
        url = reverse('user_login')
        data = {
            'idCard': '123456',
            'password': 'wrongpassword',
            'userType': '医生'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Wrong Password'})

    def test_failed_login_wrong_user_type(self):
        # 测试用户类型错误
        url = reverse('user_login')
        data = {
            'idCard': '123456',
            'password': 'password123',
            'userType': '普通用户'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Wrong Password'})

    def test_successful_registration(self):
        # 测试成功注册
        url = reverse('user_login')
        data = {
            'idCard': '987654',
            'password': 'newpassword',
            'userType': '普通用户'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully Register'})
