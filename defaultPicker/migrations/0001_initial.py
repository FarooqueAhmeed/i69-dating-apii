# Generated by Django 3.1.5 on 2022-02-27 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="age",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("age", models.IntegerField()),
            ],
            options={
                "verbose_name": "age",
                "verbose_name_plural": "age",
            },
        ),
        migrations.CreateModel(
            name="book",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "book",
                "verbose_name_plural": "book",
            },
        ),
        migrations.CreateModel(
            name="config",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
                (
                    "coinsPerMessage",
                    models.IntegerField(
                        blank=True,
                        help_text="coins deducted when user sends a message",
                        null=True,
                    ),
                ),
                (
                    "coinsPerPhotoMessage",
                    models.IntegerField(
                        blank=True,
                        help_text="coins deducted when user sends a photo message",
                        null=True,
                    ),
                ),
                (
                    "coinsPerAvatarPhoto",
                    models.IntegerField(
                        default=0,
                        help_text="coins to deduct when user uploads more than 3 photos",
                    ),
                ),
            ],
            options={
                "verbose_name": "config",
                "verbose_name_plural": "config",
            },
        ),
        migrations.CreateModel(
            name="ethnicity",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("ethnicity", models.CharField(max_length=265)),
                (
                    "ethnicity_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "ethinicty",
                "verbose_name_plural": "ethinicty",
            },
        ),
        migrations.CreateModel(
            name="family",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("familyPlans", models.CharField(max_length=265)),
                (
                    "familyPlans_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "family",
                "verbose_name_plural": "family",
            },
        ),
        migrations.CreateModel(
            name="gender",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("gender", models.CharField(max_length=265)),
                ("gender_fr", models.CharField(blank=True, max_length=265, null=True)),
            ],
            options={
                "verbose_name": "gender",
                "verbose_name_plural": "gender",
            },
        ),
        migrations.CreateModel(
            name="height",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("height", models.IntegerField()),
            ],
            options={
                "verbose_name": "height",
                "verbose_name_plural": "height",
            },
        ),
        migrations.CreateModel(
            name="interestedIn",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "interestedIn",
                "verbose_name_plural": "interestedIn",
            },
        ),
        migrations.CreateModel(
            name="movies",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "movies",
                "verbose_name_plural": "movies",
            },
        ),
        migrations.CreateModel(
            name="music",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "music",
                "verbose_name_plural": "music",
            },
        ),
        migrations.CreateModel(
            name="politics",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("politics", models.CharField(max_length=265)),
                (
                    "politics_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "politics",
                "verbose_name_plural": "politics",
            },
        ),
        migrations.CreateModel(
            name="religious",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("religious", models.CharField(max_length=265)),
                (
                    "religious_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "religious",
                "verbose_name_plural": "religious",
            },
        ),
        migrations.CreateModel(
            name="searchGender",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("searchGender", models.CharField(max_length=265)),
                (
                    "searchGender_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "searchGender",
                "verbose_name_plural": "searchGender",
            },
        ),
        migrations.CreateModel(
            name="sportsTeams",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "sportsTeams",
                "verbose_name_plural": "sportsTeams",
            },
        ),
        migrations.CreateModel(
            name="tags",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("tag", models.CharField(max_length=265)),
                ("tag_fr", models.CharField(blank=True, max_length=265, null=True)),
            ],
            options={
                "verbose_name": "tags",
                "verbose_name_plural": "tags",
            },
        ),
        migrations.CreateModel(
            name="tvShows",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("interest", models.CharField(max_length=265)),
                ("interest_fr", models.CharField(max_length=265)),
            ],
            options={
                "verbose_name": "tvShows",
                "verbose_name_plural": "tvShows",
            },
        ),
        migrations.CreateModel(
            name="zodiacSign",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("zodiacSign", models.CharField(max_length=265)),
                (
                    "zodiacSign_fr",
                    models.CharField(blank=True, max_length=265, null=True),
                ),
            ],
            options={
                "verbose_name": "zodiacSign",
                "verbose_name_plural": "zodiacSign",
            },
        ),
    ]
