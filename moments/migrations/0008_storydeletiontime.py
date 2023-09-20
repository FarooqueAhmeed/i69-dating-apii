# Generated by Django 3.1.5 on 2022-03-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0007_story"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoryDeletionTime",
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
                ("weeks", models.IntegerField()),
                ("days", models.IntegerField()),
                ("hours", models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
    ]
