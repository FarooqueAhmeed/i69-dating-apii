# Generated by Django 3.1.5 on 2022-06-14 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0023_auto_20220424_1315"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storyvisibletime",
            name="hours",
            field=models.IntegerField(default=1),
        ),
    ]
