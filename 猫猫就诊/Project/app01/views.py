import asyncio
from datetime import timedelta
import os
from urllib.parse import quote, unquote
from django.utils import timezone
import re
from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.db.models import F
from django.contrib.auth.hashers import check_password

import json

from backend import settings
from .models import *

from django.utils.deprecation import MiddlewareMixin
# Create your views here.

class MyCore(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = '*'
        if request.method == 'OPTIONS':
            response["Access-Control-Allow-Headers"] = 'Content-Type'
            response["Access-Control-Allow-Methods"] = 'POST, DELETE, PUT'
        return response

class UserView(APIView):
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
                identity_num = identity_num,
                password = pwd,
                type = type,
            )
            user.save()
            return JsonResponse({'msg': 'Successfully Register'})

class PatientView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        name = data['name']
        paymentType = data['paymentType']
        gender = data['gender']
        birthday = data['birthday']
        idType = data['idType']
        phone = data['phone']
        identity_num = data['number']
        addr = data['addr']
        patient = Patients()
        if idType == '身份证':
            patient.identity = 1
        elif idType == '医保卡':
            patient.identity = 2
        elif idType == '诊疗卡':
            patient.identity = 3
        elif idType == '护照':
            patient.identity = 4
        elif idType == '军官证':
            patient.identity = 5
        elif idType == '港澳通行证':
            patient.identity = 6
        patient.identity_num = identity_num
        patient.name = name
        if paymentType == '医保':
            patient.health_insurance = 1
        elif paymentType == '非医保':
            patient.health_insurance = 2
        if gender == '男':
            patient.gender = 1
        elif gender == '女':
            patient.gender = 2
        patient.birthday = birthday
        patient.phone_num = phone
        patient.address = addr
        patient.save()
        return JsonResponse({'msg': 'Successfully add patient'})

class RegisterView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'getRegistersData':
            return self.getRegistersData(request)
        elif action == 'cancelRegister':
            return self.cancelRegister(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    def getRegistersData(self, request):
        identity_num = json.loads(request.body)['identity_num']
        registers = []
        user = User.objects.get(identity_num=identity_num)
        if user.type == 1:
            filter = {'doctor__identity_num': identity_num}
        elif user.type == 2:
            filter = {'register': identity_num}
        for item in Register.objects.filter(**filter).annotate(
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
            doctor_name=F('doctor__name')
        ).values('id', 'queue_id', 'patient', 'patient_name', 'doctor_department',
                'doctor_name', 'time', 'position'):
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = datetime.strptime(item['time'], '%Y-%m-%d %H:%M')
            end_time = start_time + timedelta(minutes=10)
            end_time = end_time.strftime('%H:%M')
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                middle_index = len(formatted_datetime) // 2
                formatted_datetime = formatted_datetime[:middle_index] + CHINESE_AM + formatted_datetime[middle_index:]
            else:
                middle_index = len(formatted_datetime) // 2
                formatted_datetime = formatted_datetime[:middle_index] + CHINESE_PM + formatted_datetime[middle_index:]
            
            state = ""
            current_time = timezone.now()
            if start_time > current_time:
                state = "已就诊"
            else:
                state = "已预约"
            
            bill = Bill.objects.get(register=item['id']).values('price')
            registers.append({'id': item['id'],
                            'office': item['doctor_department'],
                            'orderNum': item['id'],
                            'price': bill['price'],
                            'name': item['patient_name'],
                            'cardNum': item['patient'],
                            'position': item['position'],
                            'time': formatted_datetime + '-' + end_time,
                            'line': item['queue_id'],
                            'state': state,
                            'doctor': item['doctor_name']})
        return JsonResponse({'registers': registers})

    def cancelRegister(self, request):
        id = json.loads(request.body)['id']
        item = Register.objects.get(id=id)
        Bill.objects.get(register=id).delete()
        notice = Notice()
        notice.patient = item.patient
        notice.register = item.register
        notice.doctor = item.doctor
        notice.msg_type = 2
        notice.date = datetime.date.today()
        notice.register = id
        notice.save()
        item.delete()
        return JsonResponse({'msg': "Successfully cancel register"})


class TreatmentView(APIView):
    # 返回所有就诊记录
    def get(self, request):
        treatments = []
        current_date = datetime.date.today()
        for item in Treatment.objects.annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('queue_id', 'patient_name', 'patient_birthday', 'patient_gender', 'time'):
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (item['patient_birthday'].month, item['patient_birthday'].day))
            treatments.append({
                "Id": item['queue_id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y年%m月%d日')
            })
        return JsonResponse({'treatments': treatments})
    
    def post(self, request):
        treatments = []
        identity_num = json.loads(request.body)['identity_num']
        user = User.objects.get(identity_num=identity_num)
        if user.type == 1:
            filter = {'doctor__identity_num': identity_num}
        elif user.type == 2:
            filter = {'patient': identity_num}
        for item in Treatment.objects.filter(**filter).annotate(
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
            doctor_name=F('doctor__name')
        ).values('patient_name', 'doctor_department',
                'doctor_name', 'time', 'advice', 'medicine'):
            CHINESE_AM = '上午'
            CHINESE_PM = '下午'
            start_time = datetime.strptime(item['time'], '%Y-%m-%d %H:%M')
            end_time = start_time + timedelta(minutes=10)
            end_time = end_time.strftime('%H:%M')
            formatted_datetime = start_time.strftime('%Y-%m-%d %H:%M')
            if start_time.hour < 12:
                middle_index = len(formatted_datetime) // 2
                formatted_datetime = formatted_datetime[:middle_index] + CHINESE_AM + formatted_datetime[middle_index:]
            else:
                middle_index = len(formatted_datetime) // 2
                formatted_datetime = formatted_datetime[:middle_index] + CHINESE_PM + formatted_datetime[middle_index:]
            treatments.append({'office': item['doctor_department'],
                            'time': formatted_datetime,
                            'patient': item['patient_name'],
                            'doctor': item['doctor_name'],
                            'advice': item['advice'],
                            'medicine': json.loads(item['medicine']),
            })
        return JsonResponse({'treatments': treatments})

class DoctorView(APIView):
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'upload_avatar':
            return self.upload_avatar(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    #上传医生头像, 返回该医生数据
    def upload_avatar(self, request):
        doctor = Doctors.objects.get(account=request.POST.get("account"))
        doctor.avatar = request.FILES.get('avatar')
        doctor.save()
        return JsonResponse({"doctor": doctor})

class OnDutyView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        action = data['action']
        if action == 'getNextSevenDaysDuty':
            return self.getNextSevenDaysDuty(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    # 返回一个科室接下来七天内所有医生值班情况
    def getNextSevenDaysDuty(self, request):
        duty = []
        seven_days_later = (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        department = json.loads(request.body)['department']
        for item in OnDuty.objects.filter(date__lte=seven_days_later, doctor__department=department).annotate(
            doctor_name=F('doctor__name'),
            doctor_title=F('doctor__title'),
            doctor_research=F('doctor__research'),
            doctor_avatar=F('doctor__avatar')
        ).values('doctor_id', 'doctor_name', 'doctor_title', 'date', 'doctor_research', 'doctor_avatar', 'time', 'state'):
            time = ""
            if (item['time'] == 1):
                time = "(上午)"
            elif (item['time'] == 2):
                time = "(下午)"
            else:
                time = "(晚上)"
            rest = 0
            for i in range(20):
                if not (item['state'] & (1<<i)):
                    rest += 1
            find = False
            for d in duty:
                if d['id'] == item['doctor_id']:
                    emptyTime = []
                    for i in range(20):
                        emptyTime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1<<i)) else 'full',
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
                        "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                    })
                duty.append({
                    "id": item['doctor_id'],
                    "name": item['doctor_name'],
                    "title": item['doctor_title'],
                    "research": item['doctor_research'],
                    "avatar": item['doctor_avatar'],
                    "schedule": [{'time': item['date'].strftime('%m-%d') + time,
                                    'status': 'full' if rest == 0 else 'empty',
                                    'number': rest,
                                    "emptytime": emptyTime}],
                    
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
        item_id = data['item_id']
        item = Bill.objects.get(id=item_id)
        item.state = True
        item.save()
        return self.getBillsData(request)

class NoticeView(APIView):
    def post(self, request):
        resMes = []
        billMes = []
        identity_num = json.loads(request.body)['identity_num']
        for item in Notice.objects.filter(patient=identity_num).annotate(
            doctor_name=F('doctor__name'),
            patient_name=F('patient__name'),
            doctor_department=F('doctor__department'),
        ).values('patient', 'msg_type', 'patient_name', 'doctor_department', 'treatment', 'register', 'date', 'isRead'):
            type = ""
            if item['msg_type'] == 1:
                type = "预约成功"
            elif item['msg_type'] == 2:
                type = "取消预约"
            elif item['msg_type'] == 3:
                type = "处方缴费提醒"
            else:
                type = "处方缴费成功"
            if item['msg_type'] == 1 or item['msg_type'] == 2:
                register = Register.objects.get(id=item['register'])
                resMes.append({
                    "type": type,
                    "name": item['patient_name'],
                    "department": item['doctor_department'],
                    "doctor": item['doctor_name'],
                    "time": register.time.date().strftime('%Y-%m-%d'),
                    "id": item['patient'],
                    "timetamp": item['date'],
                    "read": item['isRead']
                })
            else:
                treatment = Treatment.objects.get(id=item['treatment'])
                billMes.append({
                    "type": type,
                    "name": item['patient_name'],
                    "department": item['doctor_department'],
                    "doctor": item['doctor_name'],
                    "time": treatment.time.date().strftime('%Y-%m-%d'),
                    "id": item['patient'],
                    "timetamp": item['date'],
                    "price": treatment.price,
                    "read": item['isRead']
                })
        return JsonResponse({"resMes": resMes, "billMes": billMes})

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
            medicine = Medicine()
            medicine.name = data['name']
            if data['type'] == '3':
                medicine.medicine_type = 1
            elif data['type'] == '6':
                medicine.medicine_type = 2
            else:
                medicine.medicine_type = 3
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
            if data['type'] == '3':
                medicine.medicine_type = 1
            elif data['type'] == '6':
                medicine.medicine_type = 2
            else:
                medicine.medicine_type = 3
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
                return HttpResponse(f.read(), content_type='image/jpeg')  # 根据实际图片类型调整 content_type
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