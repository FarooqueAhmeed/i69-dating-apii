# Generated by Django 3.1.5 on 2023-02-20 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0003_auto_20220927_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAuthDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('provider', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED')], default='ENABLED', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
