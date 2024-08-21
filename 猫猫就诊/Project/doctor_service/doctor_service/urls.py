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
from doctor import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

from doctor_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/registers/list/", views.RegisterView.as_view()),
    path("api/treatments/list/", views.TreatmentView.as_view()),
    path("api/prescriptionDetailsWriteBack/", views.TreatmentView.as_view()),
    path("api/medicine/list/", views.MedicineView.as_view()),

    path("api/treatments/filter/", views.TreatmentView.as_view()),
    path("api/changeDutyState/", views.OnDutyView.as_view()),
    path("api/judgeDutyState/", views.OnDutyView.as_view()),
    path("api/duty_list/seven_days", views.OnDutyView.as_view()),
]