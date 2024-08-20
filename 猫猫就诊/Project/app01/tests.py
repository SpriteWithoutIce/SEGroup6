from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone
from .models import User, Patients, Doctors, Register, Bill, Notice, OnDuty
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
        self.patient = Patients.objects.create(
            identity_num='654321',
            name="Test_Patient",
            health_insurance=1,
            gender=1,
            birthday=date.today(),
            phone_num="1234567890",
            address="Test Address"
        )

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


class PatientViewTest(APITestCase):
    def setUp(self):
        self.existing_patient = Patients.objects.create(
            identity_num='123456',
            identity=1,
            name='Existing Patient',
            health_insurance=1,
            gender=1,
            birthday=date.today(),
            phone_num='1234567890',
            address='Existing Address'
        )
        self.valid_data = {
            'number': '654321',
            'idType': '身份证',
            'name': 'New Patient',
            'paymentType': '非医保',
            'gender': '女',
            'birthday': '1985-06-12',
            'phone': '0987654321',
            'addr': 'New Address'
        }

    # 正向测试：成功添加患者信息
    def test_successful_patient_addition(self):
        url = reverse('patient_add')
        response = self.client.post(url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully add patient'})
        patient = Patients.objects.filter(
            identity_num=self.valid_data['number']).first()
        self.assertIsNotNone(patient)

    # 负向测试：尝试用已存在的证件号码添加患者信息（增加了view.py内返回报错）
    def test_patient_addition_with_existing_number(self):
        url = reverse('patient_add')
        invalid_data = self.valid_data.copy()
        invalid_data['number'] = self.existing_patient.identity_num
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'msg': 'Error: Patient with this ID already exists.'})


class RegisterViewTest(APITestCase):
    def setUp(self):
        # 准备测试数据
        self.doctor = Doctors.objects.create(
            identity_num='1234567890',  # 证件号
            name='张三',                # 医生姓名
            title='主任医师',           # 医生职称
            department='内科',          # 医生科室
            research='心脏病研究',     # 研究方向，如果不需要可以省略或设置为None
            cost=200,                   # 出诊费，例如200元
            avatar='path/to/avatar.jpg',  # 头像图片路径，如果不需要可以省略或设置为None
            avatar_name='dr_zhang_san.jpg'  # 图片名字
        )
        self.patient = Patients.objects.create(
            identity_num='123456',
            identity=1,
            name='Existing Patient',
            health_insurance=1,
            gender=1,
            birthday=date.today(),
            phone_num='1234567890',
            address='Existing Address'
        )

    def test_get_registers_data_success(self):
        # 正向测试用例：成功获取挂号信息
        response = self.client.post(reverse('register_list'), json.dumps(
            {'action': 'getRegistersData', 'identity_num': self.doctor.identity_num}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('registers', response.json())

    def test_get_registers_data_invalid_action(self):
        # 负向测试用例：无效的 action 参数
        response = self.client.post(reverse('register_list'), json.dumps(
            {'action': 'invalid_action'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action'})

    def test_add_register_data_success(self):
        # 正向测试用例：成功添加挂号信息
        response = self.client.post(reverse('appointment_add'), json.dumps({
            'action': 'addRegisterData',
            'number': 1,
            'inumber': self.patient.identity_num,
            'identity_num': self.patient.identity_num,
            'doctorId': self.doctor.id,
            'time': "08-20-2024",
            'starttime': '09:00',
            'department': 'cat',
            'cost': 100
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': "Successfully add register"})

    def test_add_register_data_invalid_data(self):
        # 负向测试用例：使用无效数据添加挂号信息
        response = self.client.post(reverse('appointment_add'), json.dumps({
            'action': 'addRegisterData',
            'number': -1  # 无效的 queue_id
        }), content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'msg': "No such queue"})
