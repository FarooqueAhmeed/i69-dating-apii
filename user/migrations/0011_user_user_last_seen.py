# Generated by Django 3.1.5 on 2022-10-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_auto_20220607_1345"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_last_seen",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]