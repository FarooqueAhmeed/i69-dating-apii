# Generated by Django 3.1.5 on 2023-02-03 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0027_auto_20230128_1026"),
    ]

    operations = [
        migrations.CreateModel(
            name="FreeMessageLimit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField(default=0)),
            ],
        ),
    ]
