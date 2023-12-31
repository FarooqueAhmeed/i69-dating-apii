# Generated by Django 3.1.5 on 2023-01-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0040_auto_20221210_1216"),
    ]

    operations = [
        migrations.CreateModel(
            name="Settings",
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
                ("key", models.CharField(max_length=255, unique=True)),
                ("value", models.CharField(max_length=255)),
                (
                    "description",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Setting",
                "verbose_name_plural": "Settings",
            },
        ),
        migrations.AlterField(
            model_name="userlimit",
            name="action_name",
            field=models.CharField(
                choices=[
                    ("MultiStoryLimit", "MultiStoryLimit"),
                    ("FreeProfilePhotos", "FreeProfilePhotos"),
                ],
                max_length=95,
                unique=True,
            ),
        ),
    ]
