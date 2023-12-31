# Generated by Django 3.1.5 on 2022-12-02 11:09

from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0033_auto_20221129_1633"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlockedImageAlternatives",
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
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="default"),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("BLOCKED_IMG", "BLOCKED_IMG"),
                            ("IF_NO_IMAGE", "IF_NO_IMAGE"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="userphoto",
            name="is_admin_approved",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="ReviewUserPhoto",
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
                    "file",
                    models.ImageField(
                        upload_to=user.models.ReviewUserPhoto.content_file_review_name
                    ),
                ),
                (
                    "user_photo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.userphoto"
                    ),
                ),
            ],
        ),
    ]
