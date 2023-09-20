# Generated by Django 3.1.5 on 2022-06-03 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0007_broadcast_deleted"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notes",
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
                ("content", models.CharField(blank=True, max_length=5000)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "room_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.room"
                    ),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
    ]