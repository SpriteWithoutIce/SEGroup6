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
    def get(self, request):
        treatments = []

        for item in Treatment.objects.annotate(
            patient_name=F('patient__name'),
            patient_birthday=F('patient__birthday'),
            patient_gender=F('patient__gender')
        ).values('queue_id', 'patient_name', 'patient_birthday', 'patient_gender', 'date'):
            current_date = datetime.date.today()
            age = current_date.year - item['patient_birthday'].year - ((current_date.month, current_date.day) < (item['patient_birthday'].month, item['patient_birthday'].day))
            treatments.append({
                "Id": item['queue_id'],
                "name": item['patient_name'],
                "age": age,
                "sex": "男" if item['patient_gender'] == 1 else "女",
                "date": item['date'].strftime('%Y年%m月%d日')
            })

        return JsonResponse({'treatments': treatments})