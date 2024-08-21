import asyncio
from datetime import timedelta
import datetime
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

from administrator_service import settings
from .models import *

from django.utils.deprecation import MiddlewareMixin
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

class DoctorView(APIView):
    """
    api/administrator_service/doctors/list/
    获取医生列表
    Args:
        request: HTTP请求对象
    Returns:
        JsonResponse: 返回一个包含医生信息的JsonResponse对象
    """
    def get(self, request):
        doctors = []
        for item in Doctors.objects.values('identity_num', 'name', 'department',
                                        'title', 'research', 'cost', 'avatar_name'):
            doctors.append({
                'id': item['identity_num'],
                'name': item['name'],
                'office': item['department'],
                'title': item['title'],
                'research': item['research'],
                'cost': item['cost'],
                'avatar_name': item['avatar_name']
            })
        return JsonResponse({'doctors': doctors})
            
    def post(self, request):
        action = json.loads(request.body)['action']
        if action == 'upload_avatar':
            return self.upload_avatar(request)
        elif action == 'getDoctorsData':
            return self.getDoctorsData(request)
        elif action == 'deleteDoctor':
            return self.deleteDoctor(request)
        elif action == 'removeAvatar':
            return self.removeAvatar(request)
        elif action == 'addDoctor':
            return self.addDoctor(request)
        elif action == 'alterDoctor':
            return self.alterDoctor(request)
        elif action == 'searchDoctor':
            return self.searchDoctor(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
    # 上传医生头像, 返回该医生数据
    def upload_avatar(self, request):
        doctor = Doctors.objects.get(account=request.POST.get("account"))
        doctor.avatar = request.FILES.get('avatar')
        doctor.save()
        return JsonResponse({"doctor": doctor})
    
    # api/administrator_service/doctors/list/
    def getDoctorsData(self, request):
        doctors = []
        for item in Doctors.objects.values('id', 'name', 'department', 'title', 'research', 'avatar_name'):
            doctors.append({
                'id': item['id'],
                'name': item['name'],
                'department': item['department'],
                'title': item['title'],
                'research': item['research'],
                'avatar': '/api/administrator_service/doctor/avatar/' + item['avatar_name']
            }) 
        return JsonResponse({'doctors': doctors})
    
    # api/administrator_service/doctors/delete/
    def deleteDoctor(self, request):
        id = json.loads(request.body)['id']
        Doctors.objects.get(identity_num=id).delete()
        return self.get(request)
    
    # api/administrator_service/doctors/removeAvatar/
    def removeAvatar(self, request):
        avatar_name = json.loads(request.body)['avatar_name']
        file_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, avatar_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return JsonResponse({'msg': "Successfully removed avatar"})
    
    # api/administrator_service/doctors/setData/
    def addDoctor(self, request):
        data = json.loads(request.body)
        try:
            doctor = Doctors()
            doctor.name = data['name']
            doctor.title = data['title']
            doctor.department = data['department']
            doctor.cost = data['cost']
            doctor.identity_num = data['id']
            doctor.research = data['research']
            doctor.avatar_name = data['avatar_name']
            doctor.save()
            return JsonResponse({'msg': "Successfully add doctor data"})
        except Doctors.DoesNotExist:
            return JsonResponse({'msg': "Doctor with id {} not found".format(id)}, status=404)
    
    # api/administrator_service/doctors/setData/
    def alterDoctor(self, request):
        data = json.loads(request.body)
        try:
            doctor = Doctors.objects.get(identity_num=data['id'])
            doctor.name = data['name']
            doctor.title = data['title']
            doctor.department = data['department']
            doctor.cost = data['cost']
            doctor.identity_num = data['id']
            doctor.research = data['research']
            doctor.avatar_name = data['avatar_name']
            doctor.save()
            return JsonResponse({'msg': "Successfully altered doctor data"})
        except Doctors.DoesNotExist:
            return JsonResponse({'msg': "Doctor with id {} not found".format(id)}, status=404)

    def searchDoctor(self, request):
        data = json.loads(request.body)
        try:
            doctor = Doctors.objects.get(identity_num=data['identity_num'])
            return JsonResponse({'msg': "Doctor Exist", 'id': doctor.id})
        except Doctors.DoesNotExist:
            return JsonResponse({'msg': "Doctor Not Exist"})

class UploadAvatarView(APIView):
    def get(self, request, filename, *args, **kwargs):
        photo_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, filename)
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/jpeg')  # 根据实际图片类型调整 content_type
        else:
            raise Http404("Photo not found")
    
    def post(self, request):
        file = request.FILES.get('file')
        file_path = os.path.join(settings.DOCTOR_AVATAR_ROOT, file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb+') as f:
            f.write(file.read())
        url = '/api/administrator_service/doctor/avatar/' + file.name
        return JsonResponse({'msg': "Successfully uploaded photo", 'name': file.name, 'url': url})

class MedicineView(APIView):
    # api/administrator_service/medicine/list/
    def get(self, request):
        medicine = []
        for item in Medicine.objects.values('id', 'name', 'medicine_type', 'symptom', 'price', 'quantity', 'photo_name', 'symptom'):
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
    
    # api/administrator_service/medicine/delete/
    def deleteMedicine(self, request):
        id = json.loads(request.body)['id']
        Medicine.objects.get(id=id).delete()
        return self.get(request)
    
    # api/administrator_service/medicine/removePhoto/
    def removePhoto(self, request):
        photo_name = json.loads(request.body)['photo_name']
        file_path = os.path.join(settings.MEDICINE_PHOTO_ROOT, photo_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return JsonResponse({'msg': "Successfully removed photo"})
    
    # api/administrator_service/medicine/setData/
    def addMedicine(self, request):
        data = json.loads(request.body)
        try:
            medicine = Medicine()
            medicine.name = data['name']
            medicine.medicine_type = data['type']
            medicine.symptom = data['symptom']
            medicine.price = data['price']
            medicine.quantity = data['quantity']
            medicine.photo_name = data['photo_name']
            medicine.save()
            return JsonResponse({'msg': "Successfully add medicine data"})
        except Medicine.DoesNotExist:
            return JsonResponse({'msg': "Medicine with id {} not found".format(id)}, status=404)
    
    # api/administrator_service/medicine/setData/
    def alterMedicine(self, request):
        data = json.loads(request.body)
        try:
            medicine = Medicine.objects.get(id=data['id'])
            medicine.name = data['name']
            medicine.medicine_type = data['type']
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
        url = '/api/administrator_service/medicine/photo/' + file.name
        return JsonResponse({'msg': "Successfully uploaded photo", 'name': file.name, 'url': url})