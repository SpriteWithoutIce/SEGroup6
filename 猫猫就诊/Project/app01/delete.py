from django.db import connection
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
with connection.cursor() as cursor:
    cursor.execute("DROP DATABASE IF EXISTS test_seproject;")
