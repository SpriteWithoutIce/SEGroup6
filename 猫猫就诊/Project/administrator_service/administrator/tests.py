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

client = APIClient()

class DoctorViewTest(TestCase):
    def setUp(self):
        self.doctor = Doctors.objects.create(
            name='John Doe',
            title='Dr.',
            department='Cardiology',
            research='Heart diseases',
            cost=150,
            identity_num='123456',
            avatar_name='avatar1.png'
        )
        self.doctor_data = {
            'action': 'addDoctor',
            'name': 'John Doe',
            'title': 'Dr.',
            'department': 'Cardiology',
            'research': 'Heart diseases',
            'cost': 150,
            'id': '123456',
            'avatar_name': 'avatar1.png'
        }

    def test_get_doctors_positive(self):
        # 正向测试用例：获取医生列表
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.name)

    def test_get_doctors_negative(self):
        # 反向测试用例：数据库中没有医生数据
        Doctors.objects.all().delete()
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.doctor.name)

    def test_add_doctor_positive(self):
        # 正向测试用例：成功添加医生信息
        url = reverse('doctor_setdata')
        Doctors.objects.all().delete()
        response = self.client.post(
            url, self.doctor_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         'msg': "Successfully add doctor data"})

    def test_add_doctor_negative(self):
        # 反向测试用例：尝试添加已存在的医生编号
        url = reverse('doctor_setdata')
        response = self.client.post(
            url, self.doctor_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_doctor_positive(self):
        # 正向测试用例：删除存在的医生
        response = self.client.post(reverse(
            'doctor_delete'), {'action': 'deleteDoctor', 'id': self.doctor.identity_num}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_doctor_negative(self):
        # 反向测试用例：尝试删除不存在的医生
        response = self.client.post(reverse(
            'doctor_delete'), {'action': 'deleteDoctor', 'id': 'non_existent_id'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

class MedicineViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.medicine_data = {
            'name': 'Test Medicine',
            'medicine_type': 1,
            'symptom': 'Cough',
            'price': 9.99,
            'quantity': 100,
            'photo_name': 'test_photo.jpg'
        }
        self.medicine = Medicine.objects.create(**self.medicine_data)

    def test_get_medicine_list_success(self):
        # 正向测试用例：成功的获取药品列表
        url = reverse('medicine_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_medicine_list_failure_no_data(self):
        # 负向测试用例：数据库中没有药品数据
        url = reverse('medicine_list')
        Medicine.objects.all().delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_medicine_success(self):
        # 正向测试用例：成功的删除药品
        url = reverse('medicine_delete')
        response = self.client.post(url, {
            'action': 'deleteMedicine',
            'id': self.medicine.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Medicine.objects.filter(
            id=self.medicine.id).exists() is False)

    def test_delete_medicine_failure_invalid_id(self):
        # 负向测试用例：无效的药品 ID
        url = reverse('medicine_delete')
        response = self.client.post(url, {
            'action': 'deleteMedicine',
            'id': -1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_medicine_success(self):
        # 正向测试用例：成功的添加药品
        url = reverse('medicine_list')
        new_medicine_data = {
            'action': 'addMedicine',
            'name': 'Test Medicine',
            'type': 1,
            'symptom': 'Cough',
            'price': 9.99,
            'quantity': 100,
            'photo_name': 'test_photo.jpg'
        }
        new_medicine_data['name'] += ' New'
        response = self.client.post(url, json.dumps(
            new_medicine_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Medicine.objects.filter(
            name=new_medicine_data['name']).count(), 1)

    def test_add_medicine_failure_missing_data(self):
        # 负向测试用例：缺少必要的药品数据
        incomplete_data = {
            'action': 'addMedicine',
            'name': 'Incomplete Medicine',
            'type': 1
        }
        url = reverse('medicine_list')
        response = self.client.post(url, json.dumps(
            incomplete_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_medicine_success(self):
        # 正向测试用例：成功的修改药品信息
        self.medicine_data['name'] += ' Updated'
        url = reverse('medicine_setdata')
        response = self.client.post(url, {
            'action': 'alterMedicine',
            'type': 1,
            'id': self.medicine.id,
            **self.medicine_data
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Medicine.objects.get(
            id=self.medicine.id).name, self.medicine_data['name'])

    def test_alter_medicine_failure_invalid_id(self):
        # 负向测试用例：修改不存在的药品
        url = reverse('medicine_setdata')
        response = self.client.post(url, {
            'action': 'alterMedicine',
            'id': -1,
            **self.medicine_data
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 测试无效操作的测试用例可以复用 test_invalid_action 测试用例
    def test_invalid_action(self):
        # 测试用例：无效的操作
        url = reverse('medicine_list')
        response = self.client.post(url, {
            'action': 'invalid_action'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action'})