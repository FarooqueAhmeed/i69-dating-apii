# Generated by Django 3.1.5 on 2022-11-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("defaultPicker", "0006_auto_20221119_0914"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="language",
            field=models.CharField(max_length=100),
        ),
    ]
