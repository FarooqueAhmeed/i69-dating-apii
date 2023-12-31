# Generated by Django 3.1.5 on 2023-05-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0001_moved_worker_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.CharField(max_length=255)),
                ('email_port', models.PositiveIntegerField()),
                ('email_host_user', models.CharField(max_length=255)),
                ('email_host_password', models.CharField(max_length=255)),
                ('email_use_tls', models.BooleanField(default=True)),
                ('default_from_email', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Email settings',
            },
        ),
    ]
