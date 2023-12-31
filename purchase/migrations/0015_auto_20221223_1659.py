# Generated by Django 3.1.5 on 2022-12-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchase", "0014_auto_20221223_1507"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="title_am",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ar",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_az",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_be",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_bg",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_bn",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_br",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_bs",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ca",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_cs",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_da",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_de",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_el",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_es",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_es_419",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_et",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_eu",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_fa",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_fi",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_fr",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ga",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_gl",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_hi",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_hr",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_hu",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_hy",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_id",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_is",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_it",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_iw",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ja",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ka",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_km",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ko",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_la",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_lv",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_mk",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_mn",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ne",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_nl",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_nn",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_no",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_pl",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_pt_br",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_pt_pt",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ro",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ru",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sk",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sl",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sq",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sr",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sv",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_sw",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ta",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_tg",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_th",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_tl",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_tr",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_uk",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_ur",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_uz",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_vi",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_zh_cn",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="plan",
            name="title_zh_tw",
            field=models.CharField(default="", max_length=255),
        ),
    ]
