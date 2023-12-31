# Generated by Django 3.1.5 on 2022-05-25 12:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_moved_worker_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="owned_by",
            field=models.ManyToManyField(
                blank=True, related_name="fake_users", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="userrole",
            name="role",
            field=models.CharField(
                choices=[
                    ("REGULAR", "REGULAR"),
                    ("CHATTER", "CHATTER"),
                    ("ADMIN", "ADMIN"),
                    ("SUPER_ADMIN", "SUPER_ADMIN"),
                    ("FAKE_USER", "FAKE_USER"),
                ],
                default="REGULAR",
                max_length=20,
            ),
        ),
    ]
