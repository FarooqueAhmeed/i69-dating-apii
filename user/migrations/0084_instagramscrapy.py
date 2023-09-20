# Generated by Django 3.1.5 on 2023-08-31 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0083_profilevisit_last_visited_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramScrapy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('followers', models.CharField(blank=True, max_length=100, null=True)),
                ('following', models.CharField(blank=True, max_length=100, null=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('total_posts', models.CharField(blank=True, max_length=100, null=True)),
                ('posts_data', models.JSONField(blank=True, null=True)),
                ('profile_picture', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]