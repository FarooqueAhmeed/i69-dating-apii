# Generated by Django 3.1.5 on 2023-07-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0075_user_paste_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='zip_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
