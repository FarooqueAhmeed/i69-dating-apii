# Generated by Django 3.1.5 on 2022-10-26 13:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0024_auto_20220614_1910"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
