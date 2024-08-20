from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP DATABASE IF EXISTS test_seproject;")
