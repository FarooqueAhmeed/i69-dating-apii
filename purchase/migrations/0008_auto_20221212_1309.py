# Generated by Django 3.1.5 on 2022-12-12 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("purchase", "0007_auto_20221212_1201"),
    ]

    operations = [
        migrations.RenameField(
            model_name="packagepurchase",
            old_name="rennewed_at",
            new_name="renewed_at",
        ),
    ]
