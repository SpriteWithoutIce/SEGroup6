from patient_service import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from patient import views
from django.urls import path, re_path
from django.contrib import admin
import pymysql
pymysql.install_as_MySQLdb()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path('api/patient_service/patient/add/',
         views.PatientView.as_view(), name='patient_add'),
    path("api/patient_service/registers/list/", views.RegisterView.as_view()),
    path("api/patient_service/registers/cancel/", views.RegisterView.as_view()),
    path("api/patient_service/appointment/add/", views.RegisterView.as_view()),
    path("api/patient_service/register/lock/", views.RegisterView.as_view()),
    path("api/patient_service/register/unlock/", views.RegisterView.as_view()),
    path("api/patient_service/treatments/list/", views.TreatmentView.as_view()),
    path("api/patient_service/duty/next_seven_days/", views.OnDutyView.as_view()),
    path("api/patient_service/duty/all_next_seven_days/",
         views.OnDutyView.as_view()),
    path("api/patient_service/bills/list/", views.BillView.as_view()),
    path("api/patient_service/notice/list/", views.NoticeView.as_view()),

    path("api/patient_service/registers/filter/", views.RegisterView.as_view()),
    path("api/patient_service/bills/register/", views.BillView.as_view()),
    path("api/patient_service/add/bill/", views.BillView.as_view()),
    path("api/patient_service/add/Notice/", views.NoticeView.as_view()),
]
