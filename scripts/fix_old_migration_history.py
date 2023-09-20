from django.db import connection

def run():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app='notifications' and applied < '2022-04-04'")
    print("Successfully cleared old migration history")
