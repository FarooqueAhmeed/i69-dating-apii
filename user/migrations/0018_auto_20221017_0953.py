# Generated by Django 3.1.5 on 2022-10-17 09:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0017_auto_20221017_0952"),
    ]

    operations = [
        migrations.AlterField(
            model_name="moderatoronlinescheduler",
            name="moderator_list",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"roles": "MODERATOR"},
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
