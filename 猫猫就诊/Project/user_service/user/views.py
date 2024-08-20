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

from user_service import settings
from .models import *

from django.utils.deprecation import MiddlewareMixin
from patient.models import Patients
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

class UserView(APIView):
    """
    处理用户登录和注册请求
    Args:
        request: HTTP请求对象，包含请求头和请求体
    Returns:
        JsonResponse: JSON格式的响应对象，包含以下键值对：
            - msg: 字符串类型，表示操作结果，可选值为'Successfully Login'、'Wrong Password'、'Successfully Register'
    """
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
            patient = Patients.objects.using('patient_service').filter(identity_num=identity_num).first()
            if patient is None:
                patient = Patients()
                patient.identity = 1
                patient.identity_num = identity_num
                patient.name = "未填写"
                patient.health_insurance = 1
                patient.gender = 1
                patient.birthday = datetime.date.today()
                patient.phone_num = "未填写"
                patient.address = "未填写"
                patient.save(using='patient_service')
            return JsonResponse({'msg': 'Successfully Register'})