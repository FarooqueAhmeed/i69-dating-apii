# Generated by Django 3.1.5 on 2023-04-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0029_auto_20230203_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='restricted_msg',
            field=models.BooleanField(default=False),
        ),
    ]