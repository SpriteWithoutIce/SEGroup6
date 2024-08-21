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
from .models import User, Patients, Doctors, Register, Bill, Notice, OnDuty, Treatment, Medicine
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


class TreatmentViewTest(APITestCase):
    def setUp(self):
        # 创建测试数据
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
        self.register = Register.objects.create(
            queue_id=1,
            patient=self.patient,
            register=self.patient,
            doctor=self.doctor,
            time=timezone.now(),
            position="门诊大楼1楼内科"
        )
        self.data = {
            'action': 'getTreatmentsData',
            'identity_num': self.doctor.identity_num
        }

    def test_add_treatment_success(self):
        # 正向测试用例：成功添加治疗记录
        url = reverse('treatment_list')
        add_data = {
            'action': 'addTreatmentData',
            'id': self.register.id,
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

    def test_get_treatments_invalid_identity(self):
        # 负向测试用例：使用无效的 identity_num 获取治疗数据
        self.data['identity_num'] = 'invalid_identity'
        url = reverse('treatment_list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # 状态码根据业务逻辑调整
        self.assertEqual(response.json(), {
                         'error': 'Invalid doctor'})


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


class OnDutyViewTestCase(APITestCase):
    def setUp(self):
        # 设置测试数据
        self.client = APIClient()
        self.doctor = Doctors.objects.create(
            name='John Doe',
            title='Dr.',
            department='Cardiology',
            research='Heart diseases',
            cost=150,
            identity_num='123456',
            avatar_name='avatar1.png'
        )
        self.on_duty = OnDuty.objects.create(
            doctor=self.doctor,
            date=timezone.now(),
            time=1,
            state=12
        )

    def test_get_next_seven_days_duty_successful(self):
        # 正向测试用例：成功的获取接下来七天的值班情况
        url = reverse('duty_next_seven_days')
        response = self.client.post(url, {
            'action': 'getNextSevenDaysDuty',
            'department': self.doctor.department
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('duty', response.json())

    def test_get_next_seven_days_duty_fault_no_department(self):
        # 负向测试用例：缺少部门信息，导致获取失败
        url = reverse('duty_next_seven_days')
        response = self.client.post(url, {
            'action': 'getNextSevenDaysDuty'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
                         'error': 'Missing "department" key'})

    def test_get_all_next_seven_days_duty_successful(self):
        # 正向测试用例：成功的获取所有接下来七天的值班情况
        url = reverse('duty_all_next_seven_days')
        response = self.client.post(url, {
            'action': 'getAllNextSevenDaysDuty'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('duty', response.json())

    def test_get_all_next_seven_days_duty_fault_invalid_action(self):
        # 负向测试用例：无效的操作导致失败
        url = reverse('duty_all_next_seven_days')
        response = self.client.post(url, {
            'action': 'invalidAction'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action'})


class BillViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
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
        self.register = Register.objects.create(
            queue_id=1,
            patient=self.patient,
            register=self.patient,
            doctor=self.doctor,
            time=timezone.now(),
            position="门诊大楼1楼内科"
        )
        self.treatment = Treatment.objects.create(
            queue_id=self.register.queue_id,
            patient=self.patient,
            doctor=self.doctor,
            time=timezone.now(),
            advice='suggestion',
            medicine=['Aspirin', 'Paracetamol'],
            price=100
        )
        self.bill = Bill.objects.create(
            patient=self.patient,
            type=1,
            price=100,
            state=False,
            register=self.register,
            treatment=self.treatment,
            id=1
        )

    def test_get_bills_data_success(self):
        # 正向测试用例：成功的获取账单数据
        url = reverse('bill_list')  # 确保使用正确的 URL 名称
        response = self.client.post(url, {
            'action': 'getBillsData',
            'identity_num': self.patient.identity_num
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bill', response.json())

    def test_get_bills_data_failure_no_identity(self):
        # 负向测试用例：缺少身份编号，获取账单数据失败
        url = reverse('bill_list')
        response = self.client.post(url, {
            'action': 'getBillsData'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_bill_status_success(self):
        # 正向测试用例：成功的更改账单状态
        url = reverse('bill_list')
        response = self.client.post(url, {
            'action': 'changeBillStatus',
            'item_id': 1
        }, format='json')
        self.assertTrue(Bill.objects.get(id=self.bill.id).state)

    def test_change_bill_status_failure_invalid_id(self):
        # 负向测试用例：无效的账单 ID，更改账单状态失败
        url = reverse('bill_list')
        response = self.client.post(url, {
            'action': 'changeBillStatus',
            'item_id': -1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_action(self):
        # 测试用例：无效的操作
        url = reverse('bill_list')
        response = self.client.post(url, {
            'action': 'invalid_action'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action'})


class NoticeViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
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
        self.register = Register.objects.create(
            queue_id=1,
            patient=self.patient,
            register=self.patient,
            doctor=self.doctor,
            time=timezone.now(),
            position="门诊大楼1楼内科"
        )
        self.treatment = Treatment.objects.create(
            queue_id=self.register.queue_id,
            patient=self.patient,
            doctor=self.doctor,
            time=timezone.now(),
            advice='suggestion',
            medicine=['Aspirin', 'Paracetamol'],
            price=100
        )
        self.bill = Bill.objects.create(
            patient=self.patient,
            type=1,
            price=100,
            state=False,
            register=self.register,
            treatment=self.treatment,
            id=1
        )
        self.notice_unread = Notice.objects.create(
            id=1,
            patient=self.patient, doctor=self.doctor, msg_type=1, time=timezone.now(), isRead=False)
        self.notice_read = Notice.objects.create(
            id=2,
            patient=self.patient, doctor=self.doctor, msg_type=2, time=timezone.now(), isRead=True)

    def test_get_notice_data_success(self):
        # 正向测试用例：成功的获取通知数据
        url = reverse('notice_list')  # 确保使用正确的 URL 名称
        response = self.client.post(url, {
            'action': 'getMesData',
            'identity_num': self.patient.identity_num
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resMes', response.json())
        self.assertIn('billMes', response.json())

    def test_get_notice_data_failure_no_identity(self):
        # 负向测试用例：缺少身份编号，获取通知数据失败
        url = reverse('notice_list')
        response = self.client.post(url, {
            'action': 'getMesData'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Missing identity number'})

    def test_read_notice_success(self):
        # 正向测试用例：成功的标记通知为已读
        url = reverse('notice_list')
        response = self.client.post(url, {
            'action': 'readMes',
            'item_id': self.notice_unread.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'msg': 'Successfully read'})

    def test_read_notice_failure_invalid_id(self):
        # 负向测试用例：无效的通知 ID，标记通知为已读失败
        url = reverse('notice_list')
        response = self.client.post(url, {
            'action': 'readMes',
            'item_id': -1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_action(self):
        # 测试用例：无效的操作
        url = reverse('notice_list')
        response = self.client.post(url, {
            'action': 'invalid_action'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Invalid action'})


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
