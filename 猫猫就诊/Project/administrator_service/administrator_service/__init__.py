from administrator_service import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from administrator import views
from django.urls import path, re_path
from django.contrib import admin
import pymysql
pymysql.install_as_MySQLdb()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/administrator_service/doctors/getDoctor/",
         views.DoctorView.as_view(), name="getDoctor"),
    path("api/administrator_service/doctors/list/", views.DoctorView.as_view()),
    path("api/administrator_service/doctors/setData/",
         views.DoctorView.as_view(), name="setData"),
    path("api/administrator_service/doctors/removeAvatar/",
         views.DoctorView.as_view()),
    path("api/administrator_service/doctors/delete/", views.DoctorView.as_view()),
    path("api/administrator_service/doctors/uploadAvatar/",
         views.UploadAvatarView.as_view()),
    path("api/administrator_service/medicine/list/",
         views.MedicineView.as_view()),
    path("api/administrator_service/medicine/delete/",
         views.MedicineView.as_view()),
    path("api/administrator_service/medicine/uploadPhoto/",
         views.UploadPhotoView.as_view()),
    path("api/administrator_service/medicine/removePhoto/",
         views.MedicineView.as_view()),
    path("api/administrator_service/medicine/setData/",
         views.MedicineView.as_view()),

    path("api/administrator_service/doctors/exist/", views.DoctorView.as_view()),
    path("api/administrator_service/test/addDoctor/", views.DoctorView.as_view()),

    re_path(
        r'^api/administrator_service/medicine/photo/(?P<filename>[\w.-]+)$', views.UploadPhotoView.as_view()),
    re_path(
        r'^api/administrator_service/doctor/avatar/(?P<filename>[\w.-]+)$', views.UploadAvatarView.as_view()),
]
