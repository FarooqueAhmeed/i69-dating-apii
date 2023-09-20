# Generated by Django 3.1.5 on 2023-04-13 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0030_message_restricted_msg'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictedMessages',
            fields=[
            ],
            options={
                'verbose_name': '_Messages For Restricted User',
                'verbose_name_plural': '_Messages For Restricted Users',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('chat.message',),
        ),
    ]