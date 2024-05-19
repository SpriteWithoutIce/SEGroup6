from datetime import timedelta
from django.utils import timezone
import re
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.db.models import F

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

class TreatmentView(APIView):
    # 返回所有就诊记录
    def get(self, request):
        treatments = []
        current_date = datetime.date.today()
        for item in Treatment.objects.annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('queue_id', 'patient_name', 'patient_birthday', 'patient_gender', 'date'):
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (item['patient_birthday'].month, item['patient_birthday'].day))
            treatments.append({
                "Id": item['queue_id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": item['date'].strftime('%Y年%m月%d日')
            })
        return JsonResponse({'treatments': treatments})

class DoctorView(APIView):
    def post(self, request):
        action = request.POST.get('action')
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
                    emptytime = []
                    for i in range(20):
                        emptytime.append({
                            "number": i + 1,
                            "status": "empty" if not (item['state'] & (1<<i)) else 'full',
                        })
                    d['schedule'].append({'time': item['date'].strftime('%m-%d') + time,
                                        'status': 'full' if rest == 0 else 'empty',
                                        'number': rest,
                                        "emptytime": emptytime})
                    find = True
                    break
            if not find:
                emptytime = []
                for i in range(20):
                    emptytime.append({
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
                                    "emptytime": emptytime}],
                    
                })
        return JsonResponse({"duty": duty})

class MedicineView(APIView):
    def get(self, request):
        medicine = []
        for item in Medicine.objects.values('name', 'medicine_type', 'symptom', 'price'):
            type = ""
            if item['medicine_type'] == 1:
                type = "中药"
            elif item['medicine_type'] == 2:
                type = "中成药"
            else:
                type = "西药"
            medicine.append({
                "name": item['name'],
                "type": type,
                "use": item['symptom'],
                "price": item['price']
            })
        return JsonResponse({'medicine': medicine})
    
    def post(self, request):
        action = request.POST.get('action')
        if action == 'upload_photo':
            return self.upload_photo(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    # 上传药物图片
    def upload_photo(self, request):
        medicine = Medicine.objects.get(id=request.POST.get("id"))
        medicine.photo = request.FILES.get('photo')
        medicine.save()
        return JsonResponse({"medicine": medicine})