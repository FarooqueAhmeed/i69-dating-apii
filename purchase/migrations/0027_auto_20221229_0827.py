# Generated by Django 3.1.5 on 2022-12-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("purchase", "0026_permission_user_free_limit"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="packagepermissionlimit",
            options={
                "verbose_name": "Package Service Limit",
                "verbose_name_plural": "Package Service Limits",
            },
        ),
        migrations.AlterModelOptions(
            name="permission",
            options={
                "verbose_name": "Package Service",
                "verbose_name_plural": "Package Services",
            },
        ),
        migrations.AlterField(
            model_name="package",
            name="permissions",
            field=models.ManyToManyField(
                blank=True, to="purchase.Permission", verbose_name="Services"
            ),
        ),
        migrations.AlterField(
            model_name="packagepermissionlimit",
            name="permission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="permission",
                to="purchase.permission",
                verbose_name="Service",
            ),
        ),
    ]
