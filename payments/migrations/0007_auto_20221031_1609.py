# Generated by Django 3.1.5 on 2022-10-31 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0006_charges"),
    ]

    operations = [
        migrations.CreateModel(
            name="Charge",
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
                ("operation_reference", models.CharField(max_length=155)),
                ("transaction_id", models.CharField(max_length=155)),
                ("transaction_state", models.CharField(max_length=65)),
                ("latest_update", models.DateTimeField(blank=True, null=True)),
                ("price", models.FloatField()),
                (
                    "payment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="charges",
                        to="payments.bokupayment",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Charges",
        ),
    ]
