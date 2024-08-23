"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from patient import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

from patient_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path('api/patient_service/patient/add/',
         views.PatientView.as_view(), name="patient_add"),
    path("api/patient_service/registers/list/",
         views.RegisterView.as_view(), name="register_list"),
    path("api/patient_service/registers/cancel/", views.RegisterView.as_view()),
    path("api/patient_service/appointment/add/",
         views.RegisterView.as_view(), name="appointment_add"),
    path("api/patient_service/register/lock/", views.RegisterView.as_view()),
    path("api/patient_service/register/unlock/", views.RegisterView.as_view()),
    path("api/patient_service/treatments/list/", views.TreatmentView.as_view()),
    path("api/patient_service/duty/next_seven_days/", views.OnDutyView.as_view()),
    path("api/patient_service/duty/all_next_seven_days/",
         views.OnDutyView.as_view()),
    path("api/patient_service/bills/list/",
         views.BillView.as_view(), name="bill_list"),
    path("api/patient_service/notice/list/",
         views.NoticeView.as_view(), name="notice_list"),

    path("api/patient_service/registers/filter/", views.RegisterView.as_view()),
    path("api/patient_service/bills/register/", views.BillView.as_view()),
    path("api/patient_service/add/bill/", views.BillView.as_view()),
    path("api/patient_service/add/Notice/",
         views.NoticeView.as_view(), name="add_notice"),
]
