# Generated by Django 3.1.5 on 2022-11-25 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gifts", "0015_auto_20221125_1354"),
    ]

    operations = [
        migrations.CreateModel(
            name="AllGifts",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("real", "real"), ("virtual", "virtual")],
                        default="real",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="realgift",
            name="allgift",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="gifts.allgifts",
            ),
        ),
        migrations.AddField(
            model_name="virtualgift",
            name="allgift",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="gifts.allgifts",
            ),
        ),
    ]