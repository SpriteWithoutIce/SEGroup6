from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView

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
    
class PatientView(APIView):
    def get(self, request):
        patients = []

        for item in Patients.objects.all():
            patients.append(model_to_dict(item))
        return JsonResponse({'patients': patients})