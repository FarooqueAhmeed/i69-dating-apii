# Generated by Django 3.1.5 on 2023-03-03 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0056_auto_20230303_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hideuserinterestedin',
            name='region',
        ),
        migrations.AddField(
            model_name='hideuserinterestedin',
            name='region',
            field=models.ManyToManyField(to='user.Country'),
        ),
    ]
