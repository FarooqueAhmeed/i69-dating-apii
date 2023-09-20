from django.db import models
from googletrans import Translator
import time

from .utils import language_translate

translator = Translator()


class age(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    age = models.IntegerField()

    class Meta:
        verbose_name_plural = "age"
        verbose_name = "age"

    def __str__(self):
        return str(self.age)


class height(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    height = models.IntegerField()

    class Meta:
        verbose_name_plural = "height"
        verbose_name = "height"

    def __str__(self):
        return str(self.height)


class gender(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    gender = models.CharField(max_length=265)
    gender_fr = models.CharField(max_length=265, null=True, blank=True)
    gender_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    gender_nl = models.CharField(max_length=265, null=True, blank=True)
    gender_de = models.CharField(max_length=265, null=True, blank=True)
    gender_sw = models.CharField(max_length=265, null=True, blank=True)
    gender_it = models.CharField(max_length=265, null=True, blank=True)
    gender_ar = models.CharField(max_length=265, null=True, blank=True)
    gender_iw = models.CharField(max_length=265, null=True, blank=True)
    gender_ja = models.CharField(max_length=265, null=True, blank=True)
    gender_ru = models.CharField(max_length=265, null=True, blank=True)
    gender_fa = models.CharField(max_length=265, null=True, blank=True)
    gender_pt_br = models.CharField(max_length=265, null=True, blank=True)
    gender_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    gender_es = models.CharField(max_length=265, null=True, blank=True)
    gender_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gender_el = models.CharField(max_length=265, null=True, blank=True)
    gender_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    gender_uk = models.CharField(max_length=265, null=True, blank=True)
    gender_ko = models.CharField(max_length=265, null=True, blank=True)
    gender_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gender_pl = models.CharField(max_length=265, null=True, blank=True)
    gender_vi = models.CharField(max_length=265, null=True, blank=True)
    gender_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gender_no = models.CharField(max_length=265, null=True, blank=True)
    gender_sv = models.CharField(max_length=265, null=True, blank=True)
    gender_hr = models.CharField(max_length=265, null=True, blank=True)
    gender_cs = models.CharField(max_length=265, null=True, blank=True)
    gender_da = models.CharField(max_length=265, null=True, blank=True)
    gender_tl = models.CharField(max_length=265, null=True, blank=True)
    gender_fi = models.CharField(max_length=265, null=True, blank=True)
    gender_sl = models.CharField(max_length=265, null=True, blank=True)
    gender_sq = models.CharField(max_length=265, null=True, blank=True)
    gender_am = models.CharField(max_length=265, null=True, blank=True)
    gender_hy = models.CharField(max_length=265, null=True, blank=True)
    gender_la = models.CharField(max_length=265, null=True, blank=True)
    gender_lv = models.CharField(max_length=265, null=True, blank=True)
    gender_th = models.CharField(max_length=265, null=True, blank=True)
    gender_az = models.CharField(max_length=265, null=True, blank=True)
    gender_eu = models.CharField(max_length=265, null=True, blank=True)
    gender_be = models.CharField(max_length=265, null=True, blank=True)
    gender_bn = models.CharField(max_length=265, null=True, blank=True)
    gender_bs = models.CharField(max_length=265, null=True, blank=True)
    gender_bg = models.CharField(max_length=265, null=True, blank=True)
    gender_km = models.CharField(max_length=265, null=True, blank=True)
    gender_ca = models.CharField(max_length=265, null=True, blank=True)
    gender_et = models.CharField(max_length=265, null=True, blank=True)
    gender_gl = models.CharField(max_length=265, null=True, blank=True)
    gender_ka = models.CharField(max_length=265, null=True, blank=True)
    gender_hi = models.CharField(max_length=265, null=True, blank=True)
    gender_hu = models.CharField(max_length=265, null=True, blank=True)
    gender_is = models.CharField(max_length=265, null=True, blank=True)
    gender_id = models.CharField(max_length=265, null=True, blank=True)
    gender_ga = models.CharField(max_length=265, null=True, blank=True)
    gender_mk = models.CharField(max_length=265, null=True, blank=True)
    gender_mn = models.CharField(max_length=265, null=True, blank=True)
    gender_ne = models.CharField(max_length=265, null=True, blank=True)
    gender_ro = models.CharField(max_length=265, null=True, blank=True)
    gender_sr = models.CharField(max_length=265, null=True, blank=True)
    gender_sk = models.CharField(max_length=265, null=True, blank=True)
    gender_ta = models.CharField(max_length=265, null=True, blank=True)
    gender_tg = models.CharField(max_length=265, null=True, blank=True)
    gender_tr = models.CharField(max_length=265, null=True, blank=True)
    gender_ur = models.CharField(max_length=265, null=True, blank=True)
    gender_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "gender"
        verbose_name = "gender"

    def __str__(self):
        return str(self.id) + " - " + str(self.gender) + " - " + str(self.gender_fr)

    def save(self, *args, **kwargs):
        self.gender_fr = language_translate(self.gender_fr, self.gender, "fr")
        self.gender_zh_cn = language_translate(self.gender_zh_tw, self.gender, "zh-cn")
        self.gender_nl = language_translate(self.gender_nl, self.gender, "nl")
        self.gender_de = language_translate(self.gender_de, self.gender, "de")
        self.gender_sw = language_translate(self.gender_sw, self.gender, "sw")
        self.gender_it = language_translate(self.gender_it, self.gender, "it")
        self.gender_ar = language_translate(self.gender_ar, self.gender, "ar")
        self.gender_iw = language_translate(self.gender_iw, self.gender, "iw")
        self.gender_ja = language_translate(self.gender_ja, self.gender, "ja")
        self.gender_ru = language_translate(self.gender_ru, self.gender, "ru")
        self.gender_fa = language_translate(self.gender_fa, self.gender, "fa")
        self.gender_pt_br = language_translate(self.gender_pt_br, self.gender, "pt_br")
        self.gender_pt_pt = language_translate(self.gender_pt_pt, self.gender, "pt_pt")
        self.gender_es = language_translate(self.gender_es, self.gender, "es")
        self.gender_el = language_translate(self.gender_el, self.gender, "el")
        self.gender_zh_tw = language_translate(self.gender_zh_tw, self.gender, "zh-tw")
        self.gender_uk = language_translate(self.gender_uk, self.gender, "uk")
        self.gender_ko = language_translate(self.gender_ko, self.gender, "ko")
        self.gender_pl = language_translate(self.gender_pl, self.gender, "pl")
        self.gender_vi = language_translate(self.gender_vi, self.gender, "vi")
        self.gender_no = language_translate(self.gender_no, self.gender, "no")
        self.gender_sv = language_translate(self.gender_sv, self.gender, "sv")
        self.gender_hr = language_translate(self.gender_hr, self.gender, "hr")
        self.gender_cs = language_translate(self.gender_cs, self.gender, "cs")
        self.gender_da = language_translate(self.gender_da, self.gender, "da")
        self.gender_tl = language_translate(self.gender_tl, self.gender, "tl")
        self.gender_fi = language_translate(self.gender_fi, self.gender, "fi")
        self.gender_sl = language_translate(self.gender_sl, self.gender, "sl")
        self.gender_sq = language_translate(self.gender_sq, self.gender, "sq")
        self.gender_am = language_translate(self.gender_am, self.gender, "am")
        self.gender_hy = language_translate(self.gender_hy, self.gender, "hy")
        self.gender_la = language_translate(self.gender_la, self.gender, "la")
        self.gender_lv = language_translate(self.gender_lv, self.gender, "lv")
        self.gender_th = language_translate(self.gender_th, self.gender, "th")
        self.gender_az = language_translate(self.gender_az, self.gender, "az")
        self.gender_eu = language_translate(self.gender_eu, self.gender, "eu")
        self.gender_be = language_translate(self.gender_be, self.gender, "be")
        self.gender_bn = language_translate(self.gender_bn, self.gender, "bn")
        self.gender_bs = language_translate(self.gender_bs, self.gender, "bs")
        self.gender_bg = language_translate(self.gender_bg, self.gender, "bg")
        self.gender_km = language_translate(self.gender_km, self.gender, "km")
        self.gender_ca = language_translate(self.gender_ca, self.gender, "ca")
        self.gender_et = language_translate(self.gender_et, self.gender, "et")
        self.gender_gl = language_translate(self.gender_gl, self.gender, "gl")
        self.gender_ka = language_translate(self.gender_ka, self.gender, "ka")

        self.gender_hi = language_translate(self.gender_hi, self.gender, "hi")
        self.gender_hu = language_translate(self.gender_hu, self.gender, "hu")
        self.gender_is = language_translate(self.gender_is, self.gender, "is")
        self.gender_id = language_translate(self.gender_id, self.gender, "id")
        self.gender_ga = language_translate(self.gender_ga, self.gender, "ga")
        self.gender_mk = language_translate(self.gender_mk, self.gender, "mk")
        self.gender_mn = language_translate(self.gender_mn, self.gender, "mn")
        self.gender_ne = language_translate(self.gender_ne, self.gender, "ne")
        self.gender_ro = language_translate(self.gender_ro, self.gender, "ro")
        self.gender_sr = language_translate(self.gender_sr, self.gender, "sr")
        self.gender_sk = language_translate(self.gender_sk, self.gender, "sk")
        self.gender_ta = language_translate(self.gender_ta, self.gender, "ta")
        self.gender_tg = language_translate(self.gender_tg, self.gender, "tg")
        self.gender_tr = language_translate(self.gender_tr, self.gender, "tr")
        self.gender_ur = language_translate(self.gender_ur, self.gender, "ur")
        self.gender_uz = language_translate(self.gender_uz, self.gender, "uz")
        return super().save(*args, **kwargs)


class Language(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    language = models.CharField(max_length=100)
    language_code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name_plural = "language"
        verbose_name = "language"

    def __str__(self):
        return (
            str(self.id) + " - " + str(self.language) + " - " + str(self.language_code) + " - " + str(self.country_code)
        )


class searchGender(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    searchGender = models.CharField(max_length=265)
    searchGender_fr = models.CharField(max_length=265, null=True, blank=True)
    searchGender_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    searchGender_nl = models.CharField(max_length=265, null=True, blank=True)
    searchGender_de = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sw = models.CharField(max_length=265, null=True, blank=True)
    searchGender_it = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ar = models.CharField(max_length=265, null=True, blank=True)
    searchGender_iw = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ja = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ru = models.CharField(max_length=265, null=True, blank=True)
    searchGender_fa = models.CharField(max_length=265, null=True, blank=True)
    searchGender_pt_br = models.CharField(max_length=265, null=True, blank=True)
    searchGender_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    searchGender_es = models.CharField(max_length=265, null=True, blank=True)
    searchGender_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    searchGender_el = models.CharField(max_length=265, null=True, blank=True)
    searchGender_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    searchGender_uk = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ko = models.CharField(max_length=265, null=True, blank=True)
    searchGender_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    searchGender_pl = models.CharField(max_length=265, null=True, blank=True)
    searchGender_vi = models.CharField(max_length=265, null=True, blank=True)
    searchGender_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    searchGender_no = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sv = models.CharField(max_length=265, null=True, blank=True)
    searchGender_hr = models.CharField(max_length=265, null=True, blank=True)
    searchGender_cs = models.CharField(max_length=265, null=True, blank=True)
    searchGender_da = models.CharField(max_length=265, null=True, blank=True)
    searchGender_tl = models.CharField(max_length=265, null=True, blank=True)
    searchGender_fi = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sl = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sq = models.CharField(max_length=265, null=True, blank=True)
    searchGender_am = models.CharField(max_length=265, null=True, blank=True)
    searchGender_hy = models.CharField(max_length=265, null=True, blank=True)
    searchGender_la = models.CharField(max_length=265, null=True, blank=True)
    searchGender_lv = models.CharField(max_length=265, null=True, blank=True)
    searchGender_th = models.CharField(max_length=265, null=True, blank=True)
    searchGender_az = models.CharField(max_length=265, null=True, blank=True)
    searchGender_eu = models.CharField(max_length=265, null=True, blank=True)
    searchGender_be = models.CharField(max_length=265, null=True, blank=True)
    searchGender_bn = models.CharField(max_length=265, null=True, blank=True)
    searchGender_bs = models.CharField(max_length=265, null=True, blank=True)
    searchGender_bg = models.CharField(max_length=265, null=True, blank=True)
    searchGender_km = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ca = models.CharField(max_length=265, null=True, blank=True)
    searchGender_et = models.CharField(max_length=265, null=True, blank=True)
    searchGender_gl = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ka = models.CharField(max_length=265, null=True, blank=True)
    searchGender_hi = models.CharField(max_length=265, null=True, blank=True)
    searchGender_hu = models.CharField(max_length=265, null=True, blank=True)
    searchGender_is = models.CharField(max_length=265, null=True, blank=True)
    searchGender_id = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ga = models.CharField(max_length=265, null=True, blank=True)
    searchGender_mk = models.CharField(max_length=265, null=True, blank=True)
    searchGender_mn = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ne = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ro = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sr = models.CharField(max_length=265, null=True, blank=True)
    searchGender_sk = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ta = models.CharField(max_length=265, null=True, blank=True)
    searchGender_tg = models.CharField(max_length=265, null=True, blank=True)
    searchGender_tr = models.CharField(max_length=265, null=True, blank=True)
    searchGender_ur = models.CharField(max_length=265, null=True, blank=True)
    searchGender_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "searchGender"
        verbose_name = "searchGender"

    def __str__(self):
        return (
            str(self.id)
            + " - "
            + str(self.searchGender)
            + " - "
            + str(self.searchGender_fr)
        )

    def save(self, *args, **kwargs):
        self.searchGender_fr = language_translate(
            self.searchGender_fr, self.searchGender, "fr"
        )
        self.searchGender_zh_cn = language_translate(
            self.searchGender_zh_tw, self.searchGender, "zh-cn"
        )
        self.searchGender_nl = language_translate(
            self.searchGender_nl, self.searchGender, "nl"
        )
        self.searchGender_de = language_translate(
            self.searchGender_de, self.searchGender, "de"
        )
        self.searchGender_sw = language_translate(
            self.searchGender_sw, self.searchGender, "sw"
        )
        self.searchGender_it = language_translate(
            self.searchGender_it, self.searchGender, "it"
        )
        self.searchGender_ar = language_translate(
            self.searchGender_ar, self.searchGender, "ar"
        )
        self.searchGender_iw = language_translate(
            self.searchGender_iw, self.searchGender, "iw"
        )
        self.searchGender_ja = language_translate(
            self.searchGender_ja, self.searchGender, "ja"
        )
        self.searchGender_ru = language_translate(
            self.searchGender_ru, self.searchGender, "ru"
        )
        self.searchGender_fa = language_translate(
            self.searchGender_fa, self.searchGender, "fa"
        )
        self.searchGender_pt_br = language_translate(
            self.searchGender_pt_br, self.searchGender, "pt_br"
        )
        self.searchGender_pt_pt = language_translate(
            self.searchGender_pt_pt, self.searchGender, "pt_pt"
        )
        self.searchGender_es = language_translate(
            self.searchGender_es, self.searchGender, "es"
        )
        self.searchGender_el = language_translate(
            self.searchGender_el, self.searchGender, "el"
        )
        self.searchGender_zh_tw = language_translate(
            self.searchGender_zh_tw, self.searchGender, "zh-tw"
        )
        self.searchGender_uk = language_translate(
            self.searchGender_uk, self.searchGender, "uk"
        )
        self.searchGender_ko = language_translate(
            self.searchGender_ko, self.searchGender, "ko"
        )
        self.searchGender_pl = language_translate(
            self.searchGender_pl, self.searchGender, "pl"
        )
        self.searchGender_vi = language_translate(
            self.searchGender_vi, self.searchGender, "vi"
        )
        self.searchGender_no = language_translate(
            self.searchGender_no, self.searchGender, "no"
        )
        self.searchGender_sv = language_translate(
            self.searchGender_sv, self.searchGender, "sv"
        )
        self.searchGender_hr = language_translate(
            self.searchGender_hr, self.searchGender, "hr"
        )
        self.searchGender_cs = language_translate(
            self.searchGender_cs, self.searchGender, "cs"
        )
        self.searchGender_da = language_translate(
            self.searchGender_da, self.searchGender, "da"
        )
        self.searchGender_tl = language_translate(
            self.searchGender_tl, self.searchGender, "tl"
        )
        self.searchGender_fi = language_translate(
            self.searchGender_fi, self.searchGender, "fi"
        )
        self.searchGender_sl = language_translate(
            self.searchGender_sl, self.searchGender, "sl"
        )
        self.searchGender_sq = language_translate(
            self.searchGender_sq, self.searchGender, "sq"
        )
        self.searchGender_am = language_translate(
            self.searchGender_am, self.searchGender, "am"
        )
        self.searchGender_hy = language_translate(
            self.searchGender_hy, self.searchGender, "hy"
        )
        self.searchGender_la = language_translate(
            self.searchGender_la, self.searchGender, "la"
        )
        self.searchGender_lv = language_translate(
            self.searchGender_lv, self.searchGender, "lv"
        )
        self.searchGender_th = language_translate(
            self.searchGender_th, self.searchGender, "th"
        )
        self.searchGender_az = language_translate(
            self.searchGender_az, self.searchGender, "az"
        )
        self.searchGender_eu = language_translate(
            self.searchGender_eu, self.searchGender, "eu"
        )
        self.searchGender_be = language_translate(
            self.searchGender_be, self.searchGender, "be"
        )
        self.searchGender_bn = language_translate(
            self.searchGender_bn, self.searchGender, "bn"
        )
        self.searchGender_bs = language_translate(
            self.searchGender_bs, self.searchGender, "bs"
        )
        self.searchGender_bg = language_translate(
            self.searchGender_bg, self.searchGender, "bg"
        )
        self.searchGender_km = language_translate(
            self.searchGender_km, self.searchGender, "km"
        )
        self.searchGender_ca = language_translate(
            self.searchGender_ca, self.searchGender, "ca"
        )
        self.searchGender_et = language_translate(
            self.searchGender_et, self.searchGender, "et"
        )
        self.searchGender_gl = language_translate(
            self.searchGender_gl, self.searchGender, "gl"
        )
        self.searchGender_ka = language_translate(
            self.searchGender_ka, self.searchGender, "ka"
        )
        self.searchGender_hi = language_translate(
            self.searchGender_hi, self.searchGender, "hi"
        )
        self.searchGender_hu = language_translate(
            self.searchGender_hu, self.searchGender, "hu"
        )
        self.searchGender_is = language_translate(
            self.searchGender_is, self.searchGender, "is"
        )
        self.searchGender_id = language_translate(
            self.searchGender_id, self.searchGender, "id"
        )
        self.searchGender_ga = language_translate(
            self.searchGender_ga, self.searchGender, "ga"
        )
        self.searchGender_mk = language_translate(
            self.searchGender_mk, self.searchGender, "mk"
        )
        self.searchGender_mn = language_translate(
            self.searchGender_mn, self.searchGender, "mn"
        )
        self.searchGender_ne = language_translate(
            self.searchGender_ne, self.searchGender, "ne"
        )
        self.searchGender_ro = language_translate(
            self.searchGender_ro, self.searchGender, "ro"
        )
        self.searchGender_sr = language_translate(
            self.searchGender_sr, self.searchGender, "sr"
        )
        self.searchGender_sk = language_translate(
            self.searchGender_sk, self.searchGender, "sk"
        )
        self.searchGender_ta = language_translate(
            self.searchGender_ta, self.searchGender, "ta"
        )
        self.searchGender_tg = language_translate(
            self.searchGender_tg, self.searchGender, "tg"
        )
        self.searchGender_tr = language_translate(
            self.searchGender_tr, self.searchGender, "tr"
        )
        self.searchGender_ur = language_translate(
            self.searchGender_ur, self.searchGender, "ur"
        )
        self.searchGender_uz = language_translate(
            self.searchGender_uz, self.searchGender, "uz"
        )

        return super().save(*args, **kwargs)


class ethnicity(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    ethnicity = models.CharField(max_length=265)
    ethnicity_fr = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_nl = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_de = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sw = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_it = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ar = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_iw = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ja = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ru = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_fa = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_pt_br = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_es = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    ethnicity_el = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_uk = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ko = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    ethnicity_pl = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_vi = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    ethnicity_no = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sv = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_hr = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_cs = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_da = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_tl = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_fi = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sl = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sq = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_am = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_hy = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_la = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_lv = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_th = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_az = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_eu = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_be = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_bn = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_bs = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_bg = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_km = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ca = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_et = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_gl = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ka = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_hi = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_hu = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_is = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_id = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ga = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_mk = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_mn = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ne = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ro = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sr = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_sk = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ta = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_tg = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_tr = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_ur = models.CharField(max_length=265, null=True, blank=True)
    ethnicity_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "ethinicty"
        verbose_name = "ethinicty"

    def __str__(self):
        return (
            str(self.id) + " - " + str(self.ethnicity) + " - " + str(self.ethnicity_fr)
        )

    def save(self, *args, **kwargs):
        self.ethnicity_fr = language_translate(self.ethnicity_fr, self.ethnicity, "fr")
        self.ethnicity_zh_cn = language_translate(
            self.ethnicity_zh_cn, self.ethnicity, "zh-cn"
        )
        self.ethnicity_nl = language_translate(self.ethnicity_nl, self.ethnicity, "nl")
        self.ethnicity_de = language_translate(self.ethnicity_de, self.ethnicity, "de")
        self.ethnicity_sw = language_translate(self.ethnicity_sw, self.ethnicity, "sw")
        self.ethnicity_it = language_translate(self.ethnicity_it, self.ethnicity, "it")
        self.ethnicity_ar = language_translate(self.ethnicity_ar, self.ethnicity, "ar")
        self.ethnicity_iw = language_translate(self.ethnicity_iw, self.ethnicity, "iw")
        self.ethnicity_ja = language_translate(self.ethnicity_ja, self.ethnicity, "ja")
        self.ethnicity_ru = language_translate(self.ethnicity_ru, self.ethnicity, "ru")
        self.ethnicity_fa = language_translate(self.ethnicity_fa, self.ethnicity, "fa")
        self.ethnicity_pt_br = language_translate(
            self.ethnicity_pt_br, self.ethnicity, "pt_br"
        )
        self.ethnicity_pt_pt = language_translate(
            self.ethnicity_pt_pt, self.ethnicity, "pt_pt"
        )
        self.ethnicity_es = language_translate(self.ethnicity_es, self.ethnicity, "es")
        self.ethnicity_el = language_translate(self.ethnicity_el, self.ethnicity, "el")
        self.ethnicity_zh_tw = language_translate(
            self.ethnicity_zh_tw, self.ethnicity, "zh-tw"
        )
        self.ethnicity_uk = language_translate(self.ethnicity_uk, self.ethnicity, "uk")
        self.ethnicity_ko = language_translate(self.ethnicity_ko, self.ethnicity, "ko")
        self.ethnicity_pl = language_translate(self.ethnicity_pl, self.ethnicity, "pl")
        self.ethnicity_vi = language_translate(self.ethnicity_vi, self.ethnicity, "vi")
        self.ethnicity_no = language_translate(self.ethnicity_no, self.ethnicity, "no")
        self.ethnicity_sv = language_translate(self.ethnicity_sv, self.ethnicity, "sv")
        self.ethnicity_hr = language_translate(self.ethnicity_hr, self.ethnicity, "hr")
        self.ethnicity_cs = language_translate(self.ethnicity_cs, self.ethnicity, "cs")
        self.ethnicity_da = language_translate(self.ethnicity_da, self.ethnicity, "da")
        self.ethnicity_tl = language_translate(self.ethnicity_tl, self.ethnicity, "tl")
        self.ethnicity_fi = language_translate(self.ethnicity_fi, self.ethnicity, "fi")
        self.ethnicity_sl = language_translate(self.ethnicity_sl, self.ethnicity, "sl")
        self.ethnicity_sq = language_translate(self.ethnicity_sq, self.ethnicity, "sq")
        self.ethnicity_am = language_translate(self.ethnicity_am, self.ethnicity, "am")
        self.ethnicity_hy = language_translate(self.ethnicity_hy, self.ethnicity, "hy")
        self.ethnicity_la = language_translate(self.ethnicity_la, self.ethnicity, "la")
        self.ethnicity_lv = language_translate(self.ethnicity_lv, self.ethnicity, "lv")
        self.ethnicity_th = language_translate(self.ethnicity_th, self.ethnicity, "th")
        self.ethnicity_az = language_translate(self.ethnicity_az, self.ethnicity, "az")
        self.ethnicity_eu = language_translate(self.ethnicity_eu, self.ethnicity, "eu")
        self.ethnicity_be = language_translate(self.ethnicity_be, self.ethnicity, "be")
        self.ethnicity_bn = language_translate(self.ethnicity_bn, self.ethnicity, "bn")
        self.ethnicity_bs = language_translate(self.ethnicity_bs, self.ethnicity, "bs")
        self.ethnicity_bg = language_translate(self.ethnicity_bg, self.ethnicity, "bg")
        self.ethnicity_km = language_translate(self.ethnicity_km, self.ethnicity, "km")
        self.ethnicity_ca = language_translate(self.ethnicity_ca, self.ethnicity, "ca")
        self.ethnicity_et = language_translate(self.ethnicity_et, self.ethnicity, "et")
        self.ethnicity_gl = language_translate(self.ethnicity_gl, self.ethnicity, "gl")
        self.ethnicity_ka = language_translate(self.ethnicity_ka, self.ethnicity, "ka")
        self.ethnicity_hi = language_translate(self.ethnicity_hi, self.ethnicity, "hi")
        self.ethnicity_hu = language_translate(self.ethnicity_hu, self.ethnicity, "hu")
        self.ethnicity_is = language_translate(self.ethnicity_is, self.ethnicity, "is")
        self.ethnicity_id = language_translate(self.ethnicity_id, self.ethnicity, "id")
        self.ethnicity_ga = language_translate(self.ethnicity_ga, self.ethnicity, "ga")
        self.ethnicity_mk = language_translate(self.ethnicity_mk, self.ethnicity, "mk")
        self.ethnicity_mn = language_translate(self.ethnicity_mn, self.ethnicity, "mn")
        self.ethnicity_ne = language_translate(self.ethnicity_ne, self.ethnicity, "ne")
        self.ethnicity_ro = language_translate(self.ethnicity_ro, self.ethnicity, "ro")
        self.ethnicity_sr = language_translate(self.ethnicity_sr, self.ethnicity, "sr")
        self.ethnicity_sk = language_translate(self.ethnicity_sk, self.ethnicity, "sk")
        self.ethnicity_ta = language_translate(self.ethnicity_ta, self.ethnicity, "ta")
        self.ethnicity_tg = language_translate(self.ethnicity_tg, self.ethnicity, "tg")
        self.ethnicity_tr = language_translate(self.ethnicity_tr, self.ethnicity, "tr")
        self.ethnicity_ur = language_translate(self.ethnicity_ur, self.ethnicity, "ur")
        self.ethnicity_uz = language_translate(self.ethnicity_uz, self.ethnicity, "uz")

        return super().save(*args, **kwargs)


class family(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    familyPlans = models.CharField(max_length=265)
    familyPlans_fr = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_nl = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_de = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sw = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_it = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ar = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_iw = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ja = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ru = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_fa = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_pt_br = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_es = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    familyPlans_el = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_uk = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ko = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    familyPlans_pl = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_vi = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    familyPlans_no = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sv = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_hr = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_cs = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_da = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_tl = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_fi = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sl = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sq = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_am = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_hy = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_la = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_lv = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_th = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_az = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_eu = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_be = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_bn = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_bs = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_bg = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_km = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ca = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_et = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_gl = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ka = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_hi = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_hu = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_is = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_id = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ga = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_mk = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_mn = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ne = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ro = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sr = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_sk = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ta = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_tg = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_tr = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_ur = models.CharField(max_length=265, null=True, blank=True)
    familyPlans_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "family"
        verbose_name = "family"

    def __str__(self):
        return (
            str(self.id)
            + " - "
            + str(self.familyPlans)
            + " - "
            + str(self.familyPlans_fr)
        )

    def save(self, *args, **kwargs):
        self.familyPlans_fr = language_translate(
            self.familyPlans_fr, self.familyPlans, "fr"
        )
        self.familyPlans_zh_cn = language_translate(
            self.familyPlans_zh_cn, self.familyPlans, "zh-cn"
        )
        self.familyPlans_nl = language_translate(
            self.familyPlans_nl, self.familyPlans, "nl"
        )
        self.familyPlans_de = language_translate(
            self.familyPlans_de, self.familyPlans, "de"
        )
        self.familyPlans_sw = language_translate(
            self.familyPlans_sw, self.familyPlans, "sw"
        )
        self.familyPlans_it = language_translate(
            self.familyPlans_it, self.familyPlans, "it"
        )
        self.familyPlans_ar = language_translate(
            self.familyPlans_ar, self.familyPlans, "ar"
        )
        self.familyPlans_iw = language_translate(
            self.familyPlans_iw, self.familyPlans, "iw"
        )
        self.familyPlans_ja = language_translate(
            self.familyPlans_ja, self.familyPlans, "ja"
        )
        self.familyPlans_ru = language_translate(
            self.familyPlans_ru, self.familyPlans, "ru"
        )
        self.familyPlans_fa = language_translate(
            self.familyPlans_fa, self.familyPlans, "fa"
        )
        self.familyPlans_pt_br = language_translate(
            self.familyPlans_pt_br, self.familyPlans, "pt_br"
        )
        self.familyPlans_pt_pt = language_translate(
            self.familyPlans_pt_pt, self.familyPlans, "pt_pt"
        )
        self.familyPlans_es = language_translate(
            self.familyPlans_es, self.familyPlans, "es"
        )
        self.familyPlans_el = language_translate(
            self.familyPlans_el, self.familyPlans, "el"
        )
        self.familyPlans_zh_tw = language_translate(
            self.familyPlans_zh_tw, self.familyPlans, "zh-tw"
        )
        self.familyPlans_uk = language_translate(
            self.familyPlans_uk, self.familyPlans, "uk"
        )
        self.familyPlans_ko = language_translate(
            self.familyPlans_ko, self.familyPlans, "ko"
        )
        self.familyPlans_pl = language_translate(
            self.familyPlans_pl, self.familyPlans, "pl"
        )
        self.familyPlans_vi = language_translate(
            self.familyPlans_vi, self.familyPlans, "vi"
        )
        self.familyPlans_no = language_translate(
            self.familyPlans_no, self.familyPlans, "no"
        )
        self.familyPlans_sv = language_translate(
            self.familyPlans_sv, self.familyPlans, "sv"
        )
        self.familyPlans_hr = language_translate(
            self.familyPlans_hr, self.familyPlans, "hr"
        )
        self.familyPlans_cs = language_translate(
            self.familyPlans_cs, self.familyPlans, "cs"
        )
        self.familyPlans_da = language_translate(
            self.familyPlans_da, self.familyPlans, "da"
        )
        self.familyPlans_tl = language_translate(
            self.familyPlans_tl, self.familyPlans, "tl"
        )
        self.familyPlans_fi = language_translate(
            self.familyPlans_fi, self.familyPlans, "fi"
        )
        self.familyPlans_sl = language_translate(
            self.familyPlans_sl, self.familyPlans, "sl"
        )
        self.familyPlans_sq = language_translate(
            self.familyPlans_sq, self.familyPlans, "sq"
        )
        self.familyPlans_am = language_translate(
            self.familyPlans_am, self.familyPlans, "am"
        )
        self.familyPlans_hy = language_translate(
            self.familyPlans_hy, self.familyPlans, "hy"
        )
        self.familyPlans_la = language_translate(
            self.familyPlans_la, self.familyPlans, "la"
        )
        self.familyPlans_lv = language_translate(
            self.familyPlans_lv, self.familyPlans, "lv"
        )
        self.familyPlans_th = language_translate(
            self.familyPlans_th, self.familyPlans, "th"
        )
        self.familyPlans_az = language_translate(
            self.familyPlans_az, self.familyPlans, "az"
        )
        self.familyPlans_eu = language_translate(
            self.familyPlans_eu, self.familyPlans, "eu"
        )
        self.familyPlans_be = language_translate(
            self.familyPlans_be, self.familyPlans, "be"
        )
        self.familyPlans_bn = language_translate(
            self.familyPlans_bn, self.familyPlans, "bn"
        )
        self.familyPlans_bs = language_translate(
            self.familyPlans_bs, self.familyPlans, "bs"
        )
        self.familyPlans_bg = language_translate(
            self.familyPlans_bg, self.familyPlans, "bg"
        )
        self.familyPlans_km = language_translate(
            self.familyPlans_km, self.familyPlans, "km"
        )
        self.familyPlans_ca = language_translate(
            self.familyPlans_ca, self.familyPlans, "ca"
        )
        self.familyPlans_et = language_translate(
            self.familyPlans_et, self.familyPlans, "et"
        )
        self.familyPlans_gl = language_translate(
            self.familyPlans_gl, self.familyPlans, "gl"
        )
        self.familyPlans_ka = language_translate(
            self.familyPlans_ka, self.familyPlans, "ka"
        )
        self.familyPlans_hi = language_translate(
            self.familyPlans_hi, self.familyPlans, "hi"
        )
        self.familyPlans_hu = language_translate(
            self.familyPlans_hu, self.familyPlans, "hu"
        )
        self.familyPlans_is = language_translate(
            self.familyPlans_is, self.familyPlans, "is"
        )
        self.familyPlans_id = language_translate(
            self.familyPlans_id, self.familyPlans, "id"
        )
        self.familyPlans_ga = language_translate(
            self.familyPlans_ga, self.familyPlans, "ga"
        )
        self.familyPlans_mk = language_translate(
            self.familyPlans_mk, self.familyPlans, "mk"
        )
        self.familyPlans_mn = language_translate(
            self.familyPlans_mn, self.familyPlans, "mn"
        )
        self.familyPlans_ne = language_translate(
            self.familyPlans_ne, self.familyPlans, "ne"
        )
        self.familyPlans_ro = language_translate(
            self.familyPlans_ro, self.familyPlans, "ro"
        )
        self.familyPlans_sr = language_translate(
            self.familyPlans_sr, self.familyPlans, "sr"
        )
        self.familyPlans_sk = language_translate(
            self.familyPlans_sk, self.familyPlans, "sk"
        )
        self.familyPlans_ta = language_translate(
            self.familyPlans_ta, self.familyPlans, "ta"
        )
        self.familyPlans_tg = language_translate(
            self.familyPlans_tg, self.familyPlans, "tg"
        )
        self.familyPlans_tr = language_translate(
            self.familyPlans_tr, self.familyPlans, "tr"
        )
        self.familyPlans_ur = language_translate(
            self.familyPlans_ur, self.familyPlans, "ur"
        )
        self.familyPlans_uz = language_translate(
            self.familyPlans_uz, self.familyPlans, "uz"
        )

        return super().save(*args, **kwargs)


class politics(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    politics = models.CharField(max_length=265)
    politics_fr = models.CharField(max_length=265, null=True, blank=True)
    politics_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    politics_nl = models.CharField(max_length=265, null=True, blank=True)
    politics_de = models.CharField(max_length=265, null=True, blank=True)
    politics_sw = models.CharField(max_length=265, null=True, blank=True)
    politics_it = models.CharField(max_length=265, null=True, blank=True)
    politics_ar = models.CharField(max_length=265, null=True, blank=True)
    politics_iw = models.CharField(max_length=265, null=True, blank=True)
    politics_ja = models.CharField(max_length=265, null=True, blank=True)
    politics_ru = models.CharField(max_length=265, null=True, blank=True)
    politics_fa = models.CharField(max_length=265, null=True, blank=True)
    politics_pt_br = models.CharField(max_length=265, null=True, blank=True)
    politics_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    politics_es = models.CharField(max_length=265, null=True, blank=True)
    politics_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    politics_el = models.CharField(max_length=265, null=True, blank=True)
    politics_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    politics_uk = models.CharField(max_length=265, null=True, blank=True)
    politics_ko = models.CharField(max_length=265, null=True, blank=True)
    politics_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    politics_pl = models.CharField(max_length=265, null=True, blank=True)
    politics_vi = models.CharField(max_length=265, null=True, blank=True)
    politics_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    politics_no = models.CharField(max_length=265, null=True, blank=True)
    politics_sv = models.CharField(max_length=265, null=True, blank=True)
    politics_hr = models.CharField(max_length=265, null=True, blank=True)
    politics_cs = models.CharField(max_length=265, null=True, blank=True)
    politics_da = models.CharField(max_length=265, null=True, blank=True)
    politics_tl = models.CharField(max_length=265, null=True, blank=True)
    politics_fi = models.CharField(max_length=265, null=True, blank=True)
    politics_sl = models.CharField(max_length=265, null=True, blank=True)
    politics_sq = models.CharField(max_length=265, null=True, blank=True)
    politics_am = models.CharField(max_length=265, null=True, blank=True)
    politics_hy = models.CharField(max_length=265, null=True, blank=True)
    politics_la = models.CharField(max_length=265, null=True, blank=True)
    politics_lv = models.CharField(max_length=265, null=True, blank=True)
    politics_th = models.CharField(max_length=265, null=True, blank=True)
    politics_az = models.CharField(max_length=265, null=True, blank=True)
    politics_eu = models.CharField(max_length=265, null=True, blank=True)
    politics_be = models.CharField(max_length=265, null=True, blank=True)
    politics_bn = models.CharField(max_length=265, null=True, blank=True)
    politics_bs = models.CharField(max_length=265, null=True, blank=True)
    politics_bg = models.CharField(max_length=265, null=True, blank=True)
    politics_km = models.CharField(max_length=265, null=True, blank=True)
    politics_ca = models.CharField(max_length=265, null=True, blank=True)
    politics_et = models.CharField(max_length=265, null=True, blank=True)
    politics_gl = models.CharField(max_length=265, null=True, blank=True)
    politics_ka = models.CharField(max_length=265, null=True, blank=True)
    politics_hi = models.CharField(max_length=265, null=True, blank=True)
    politics_hu = models.CharField(max_length=265, null=True, blank=True)
    politics_is = models.CharField(max_length=265, null=True, blank=True)
    politics_id = models.CharField(max_length=265, null=True, blank=True)
    politics_ga = models.CharField(max_length=265, null=True, blank=True)
    politics_mk = models.CharField(max_length=265, null=True, blank=True)
    politics_mn = models.CharField(max_length=265, null=True, blank=True)
    politics_ne = models.CharField(max_length=265, null=True, blank=True)
    politics_ro = models.CharField(max_length=265, null=True, blank=True)
    politics_sr = models.CharField(max_length=265, null=True, blank=True)
    politics_sk = models.CharField(max_length=265, null=True, blank=True)
    politics_ta = models.CharField(max_length=265, null=True, blank=True)
    politics_tg = models.CharField(max_length=265, null=True, blank=True)
    politics_tr = models.CharField(max_length=265, null=True, blank=True)
    politics_ur = models.CharField(max_length=265, null=True, blank=True)
    politics_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "politics"
        verbose_name = "politics"

    def __str__(self):
        return str(self.id) + " - " + str(self.politics) + " - " + str(self.politics_fr)

    def save(self, *args, **kwargs):
        self.politics_fr = language_translate(self.politics_fr, self.politics, "fr")
        self.politics_zh_cn = language_translate(
            self.politics_zh_cn, self.politics, "zh-cn"
        )
        self.politics_nl = language_translate(self.politics_nl, self.politics, "nl")
        self.politics_de = language_translate(self.politics_de, self.politics, "de")
        self.politics_sw = language_translate(self.politics_sw, self.politics, "sw")
        self.politics_it = language_translate(self.politics_it, self.politics, "it")
        self.politics_ar = language_translate(self.politics_ar, self.politics, "ar")
        self.politics_iw = language_translate(self.politics_iw, self.politics, "iw")
        self.politics_ja = language_translate(self.politics_ja, self.politics, "ja")
        self.politics_ru = language_translate(self.politics_ru, self.politics, "ru")
        self.politics_fa = language_translate(self.politics_fa, self.politics, "fa")
        self.politics_pt_br = language_translate(
            self.politics_pt_br, self.politics, "pt_br"
        )
        self.politics_pt_pt = language_translate(
            self.politics_pt_pt, self.politics, "pt_pt"
        )
        self.politics_es = language_translate(self.politics_es, self.politics, "es")
        self.politics_el = language_translate(self.politics_el, self.politics, "el")
        self.politics_zh_tw = language_translate(
            self.politics_zh_tw, self.politics, "zh-tw"
        )
        self.politics_uk = language_translate(self.politics_uk, self.politics, "uk")
        self.politics_ko = language_translate(self.politics_ko, self.politics, "ko")
        self.politics_pl = language_translate(self.politics_pl, self.politics, "pl")
        self.politics_vi = language_translate(self.politics_vi, self.politics, "vi")
        self.politics_no = language_translate(self.politics_no, self.politics, "no")
        self.politics_sv = language_translate(self.politics_sv, self.politics, "sv")
        self.politics_hr = language_translate(self.politics_hr, self.politics, "hr")
        self.politics_cs = language_translate(self.politics_cs, self.politics, "cs")
        self.politics_da = language_translate(self.politics_da, self.politics, "da")
        self.politics_tl = language_translate(self.politics_tl, self.politics, "tl")
        self.politics_fi = language_translate(self.politics_fi, self.politics, "fi")
        self.politics_sl = language_translate(self.politics_sl, self.politics, "sl")
        self.politics_sq = language_translate(self.politics_sq, self.politics, "sq")
        self.politics_am = language_translate(self.politics_am, self.politics, "am")
        self.politics_hy = language_translate(self.politics_hy, self.politics, "hy")
        self.politics_la = language_translate(self.politics_la, self.politics, "la")
        self.politics_lv = language_translate(self.politics_lv, self.politics, "lv")
        self.politics_th = language_translate(self.politics_th, self.politics, "th")
        self.politics_az = language_translate(self.politics_az, self.politics, "az")
        self.politics_eu = language_translate(self.politics_eu, self.politics, "eu")
        self.politics_be = language_translate(self.politics_be, self.politics, "be")
        self.politics_bn = language_translate(self.politics_bn, self.politics, "bn")
        self.politics_bs = language_translate(self.politics_bs, self.politics, "bs")
        self.politics_bg = language_translate(self.politics_bg, self.politics, "bg")
        self.politics_km = language_translate(self.politics_km, self.politics, "km")
        self.politics_ca = language_translate(self.politics_ca, self.politics, "ca")
        self.politics_et = language_translate(self.politics_et, self.politics, "et")
        self.politics_gl = language_translate(self.politics_gl, self.politics, "gl")
        self.politics_ka = language_translate(self.politics_ka, self.politics, "ka")
        self.politics_hi = language_translate(self.politics_hi, self.politics, "hi")
        self.politics_hu = language_translate(self.politics_hu, self.politics, "hu")
        self.politics_is = language_translate(self.politics_is, self.politics, "is")
        self.politics_id = language_translate(self.politics_id, self.politics, "id")
        self.politics_ga = language_translate(self.politics_ga, self.politics, "ga")
        self.politics_mk = language_translate(self.politics_mk, self.politics, "mk")
        self.politics_mn = language_translate(self.politics_mn, self.politics, "mn")
        self.politics_ne = language_translate(self.politics_ne, self.politics, "ne")
        self.politics_ro = language_translate(self.politics_ro, self.politics, "ro")
        self.politics_sr = language_translate(self.politics_sr, self.politics, "sr")
        self.politics_sk = language_translate(self.politics_sk, self.politics, "sk")
        self.politics_ta = language_translate(self.politics_ta, self.politics, "ta")
        self.politics_tg = language_translate(self.politics_tg, self.politics, "tg")
        self.politics_tr = language_translate(self.politics_tr, self.politics, "tr")
        self.politics_ur = language_translate(self.politics_ur, self.politics, "ur")
        self.politics_uz = language_translate(self.politics_uz, self.politics, "uz")

        return super().save(*args, **kwargs)


class religious(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    religious = models.CharField(max_length=265)
    religious_fr = models.CharField(max_length=265, null=True, blank=True)
    religious_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    religious_nl = models.CharField(max_length=265, null=True, blank=True)
    religious_de = models.CharField(max_length=265, null=True, blank=True)
    religious_sw = models.CharField(max_length=265, null=True, blank=True)
    religious_it = models.CharField(max_length=265, null=True, blank=True)
    religious_ar = models.CharField(max_length=265, null=True, blank=True)
    religious_iw = models.CharField(max_length=265, null=True, blank=True)
    religious_ja = models.CharField(max_length=265, null=True, blank=True)
    religious_ru = models.CharField(max_length=265, null=True, blank=True)
    religious_fa = models.CharField(max_length=265, null=True, blank=True)
    religious_pt_br = models.CharField(max_length=265, null=True, blank=True)
    religious_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    religious_es = models.CharField(max_length=265, null=True, blank=True)
    religious_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    religious_el = models.CharField(max_length=265, null=True, blank=True)
    religious_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    religious_uk = models.CharField(max_length=265, null=True, blank=True)
    religious_ko = models.CharField(max_length=265, null=True, blank=True)
    religious_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    religious_pl = models.CharField(max_length=265, null=True, blank=True)
    religious_vi = models.CharField(max_length=265, null=True, blank=True)
    religious_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    religious_no = models.CharField(max_length=265, null=True, blank=True)
    religious_sv = models.CharField(max_length=265, null=True, blank=True)
    religious_hr = models.CharField(max_length=265, null=True, blank=True)
    religious_cs = models.CharField(max_length=265, null=True, blank=True)
    religious_da = models.CharField(max_length=265, null=True, blank=True)
    religious_tl = models.CharField(max_length=265, null=True, blank=True)
    religious_fi = models.CharField(max_length=265, null=True, blank=True)
    religious_sl = models.CharField(max_length=265, null=True, blank=True)
    religious_sq = models.CharField(max_length=265, null=True, blank=True)
    religious_am = models.CharField(max_length=265, null=True, blank=True)
    religious_hy = models.CharField(max_length=265, null=True, blank=True)
    religious_la = models.CharField(max_length=265, null=True, blank=True)
    religious_lv = models.CharField(max_length=265, null=True, blank=True)
    religious_th = models.CharField(max_length=265, null=True, blank=True)
    religious_az = models.CharField(max_length=265, null=True, blank=True)
    religious_eu = models.CharField(max_length=265, null=True, blank=True)
    religious_be = models.CharField(max_length=265, null=True, blank=True)
    religious_bn = models.CharField(max_length=265, null=True, blank=True)
    religious_bs = models.CharField(max_length=265, null=True, blank=True)
    religious_bg = models.CharField(max_length=265, null=True, blank=True)
    religious_km = models.CharField(max_length=265, null=True, blank=True)
    religious_ca = models.CharField(max_length=265, null=True, blank=True)
    religious_et = models.CharField(max_length=265, null=True, blank=True)
    religious_gl = models.CharField(max_length=265, null=True, blank=True)
    religious_ka = models.CharField(max_length=265, null=True, blank=True)
    religious_hi = models.CharField(max_length=265, null=True, blank=True)
    religious_hu = models.CharField(max_length=265, null=True, blank=True)
    religious_is = models.CharField(max_length=265, null=True, blank=True)
    religious_id = models.CharField(max_length=265, null=True, blank=True)
    religious_ga = models.CharField(max_length=265, null=True, blank=True)
    religious_mk = models.CharField(max_length=265, null=True, blank=True)
    religious_mn = models.CharField(max_length=265, null=True, blank=True)
    religious_ne = models.CharField(max_length=265, null=True, blank=True)
    religious_ro = models.CharField(max_length=265, null=True, blank=True)
    religious_sr = models.CharField(max_length=265, null=True, blank=True)
    religious_sk = models.CharField(max_length=265, null=True, blank=True)
    religious_ta = models.CharField(max_length=265, null=True, blank=True)
    religious_tg = models.CharField(max_length=265, null=True, blank=True)
    religious_tr = models.CharField(max_length=265, null=True, blank=True)
    religious_ur = models.CharField(max_length=265, null=True, blank=True)
    religious_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "religious"
        verbose_name = "religious"

    def __str__(self):
        return (
            str(self.id) + " - " + str(self.religious) + " - " + str(self.religious_fr)
        )

    def save(self, *args, **kwargs):
        self.religious_fr = language_translate(self.religious_fr, self.religious, "fr")
        self.religious_zh_cn = language_translate(
            self.religious_zh_cn, self.religious, "zh-cn"
        )
        self.religious_nl = language_translate(self.religious_nl, self.religious, "nl")
        self.religious_de = language_translate(self.religious_de, self.religious, "de")
        self.religious_sw = language_translate(self.religious_sw, self.religious, "sw")
        self.religious_it = language_translate(self.religious_it, self.religious, "it")
        self.religious_ar = language_translate(self.religious_ar, self.religious, "ar")
        self.religious_iw = language_translate(self.religious_iw, self.religious, "iw")
        self.religious_ja = language_translate(self.religious_ja, self.religious, "ja")
        self.religious_ru = language_translate(self.religious_ru, self.religious, "ru")
        self.religious_fa = language_translate(self.religious_fa, self.religious, "fa")
        self.religious_pt_br = language_translate(
            self.religious_pt_br, self.religious, "pt_br"
        )
        self.religious_pt_pt = language_translate(
            self.religious_pt_pt, self.religious, "pt_pt"
        )
        self.religious_es = language_translate(self.religious_es, self.religious, "es")
        self.religious_el = language_translate(self.religious_el, self.religious, "el")
        self.religious_zh_tw = language_translate(
            self.religious_zh_tw, self.religious, "zh-tw"
        )
        self.religious_uk = language_translate(self.religious_uk, self.religious, "uk")
        self.religious_ko = language_translate(self.religious_ko, self.religious, "ko")
        self.religious_pl = language_translate(self.religious_pl, self.religious, "pl")
        self.religious_vi = language_translate(self.religious_vi, self.religious, "vi")
        self.religious_no = language_translate(self.religious_no, self.religious, "no")
        self.religious_sv = language_translate(self.religious_sv, self.religious, "sv")
        self.religious_hr = language_translate(self.religious_hr, self.religious, "hr")
        self.religious_cs = language_translate(self.religious_cs, self.religious, "cs")
        self.religious_da = language_translate(self.religious_da, self.religious, "da")
        self.religious_tl = language_translate(self.religious_tl, self.religious, "tl")
        self.religious_fi = language_translate(self.religious_fi, self.religious, "fi")
        self.religious_sl = language_translate(self.religious_sl, self.religious, "sl")
        self.religious_sq = language_translate(self.religious_sq, self.religious, "sq")
        self.religious_am = language_translate(self.religious_am, self.religious, "am")
        self.religious_hy = language_translate(self.religious_hy, self.religious, "hy")
        self.religious_la = language_translate(self.religious_la, self.religious, "la")
        self.religious_lv = language_translate(self.religious_lv, self.religious, "lv")
        self.religious_th = language_translate(self.religious_th, self.religious, "th")
        self.religious_az = language_translate(self.religious_az, self.religious, "az")
        self.religious_eu = language_translate(self.religious_eu, self.religious, "eu")
        self.religious_be = language_translate(self.religious_be, self.religious, "be")
        self.religious_bn = language_translate(self.religious_bn, self.religious, "bn")
        self.religious_bs = language_translate(self.religious_bs, self.religious, "bs")
        self.religious_bg = language_translate(self.religious_bg, self.religious, "bg")
        self.religious_km = language_translate(self.religious_km, self.religious, "km")
        self.religious_ca = language_translate(self.religious_ca, self.religious, "ca")
        self.religious_et = language_translate(self.religious_et, self.religious, "et")
        self.religious_gl = language_translate(self.religious_gl, self.religious, "gl")
        self.religious_ka = language_translate(self.religious_ka, self.religious, "ka")
        self.religious_hi = language_translate(self.religious_hi, self.religious, "hi")
        self.religious_hu = language_translate(self.religious_hu, self.religious, "hu")
        self.religious_is = language_translate(self.religious_is, self.religious, "is")
        self.religious_id = language_translate(self.religious_id, self.religious, "id")
        self.religious_ga = language_translate(self.religious_ga, self.religious, "ga")
        self.religious_mk = language_translate(self.religious_mk, self.religious, "mk")
        self.religious_mn = language_translate(self.religious_mn, self.religious, "mn")
        self.religious_ne = language_translate(self.religious_ne, self.religious, "ne")
        self.religious_ro = language_translate(self.religious_ro, self.religious, "ro")
        self.religious_sr = language_translate(self.religious_sr, self.religious, "sr")
        self.religious_sk = language_translate(self.religious_sk, self.religious, "sk")
        self.religious_ta = language_translate(self.religious_ta, self.religious, "ta")
        self.religious_tg = language_translate(self.religious_tg, self.religious, "tg")
        self.religious_tr = language_translate(self.religious_tr, self.religious, "tr")
        self.religious_ur = language_translate(self.religious_ur, self.religious, "ur")
        self.religious_uz = language_translate(self.religious_uz, self.religious, "uz")

        return super().save(*args, **kwargs)


class tags(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    tag = models.CharField(max_length=265)
    tag_fr = models.CharField(max_length=265, null=True, blank=True)
    tag_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    tag_nl = models.CharField(max_length=265, null=True, blank=True)
    tag_de = models.CharField(max_length=265, null=True, blank=True)
    tag_sw = models.CharField(max_length=265, null=True, blank=True)
    tag_it = models.CharField(max_length=265, null=True, blank=True)
    tag_ar = models.CharField(max_length=265, null=True, blank=True)
    tag_iw = models.CharField(max_length=265, null=True, blank=True)
    tag_ja = models.CharField(max_length=265, null=True, blank=True)
    tag_ru = models.CharField(max_length=265, null=True, blank=True)
    tag_fa = models.CharField(max_length=265, null=True, blank=True)
    tag_pt_br = models.CharField(max_length=265, null=True, blank=True)
    tag_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    tag_es = models.CharField(max_length=265, null=True, blank=True)
    tag_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    tag_el = models.CharField(max_length=265, null=True, blank=True)
    tag_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    tag_uk = models.CharField(max_length=265, null=True, blank=True)
    tag_ko = models.CharField(max_length=265, null=True, blank=True)
    tag_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    tag_pl = models.CharField(max_length=265, null=True, blank=True)
    tag_vi = models.CharField(max_length=265, null=True, blank=True)
    tag_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    tag_no = models.CharField(max_length=265, null=True, blank=True)
    tag_sv = models.CharField(max_length=265, null=True, blank=True)
    tag_hr = models.CharField(max_length=265, null=True, blank=True)
    tag_cs = models.CharField(max_length=265, null=True, blank=True)
    tag_da = models.CharField(max_length=265, null=True, blank=True)
    tag_tl = models.CharField(max_length=265, null=True, blank=True)
    tag_fi = models.CharField(max_length=265, null=True, blank=True)
    tag_sl = models.CharField(max_length=265, null=True, blank=True)
    tag_sq = models.CharField(max_length=265, null=True, blank=True)
    tag_am = models.CharField(max_length=265, null=True, blank=True)
    tag_hy = models.CharField(max_length=265, null=True, blank=True)
    tag_la = models.CharField(max_length=265, null=True, blank=True)
    tag_lv = models.CharField(max_length=265, null=True, blank=True)
    tag_th = models.CharField(max_length=265, null=True, blank=True)
    tag_az = models.CharField(max_length=265, null=True, blank=True)
    tag_eu = models.CharField(max_length=265, null=True, blank=True)
    tag_be = models.CharField(max_length=265, null=True, blank=True)
    tag_bn = models.CharField(max_length=265, null=True, blank=True)
    tag_bs = models.CharField(max_length=265, null=True, blank=True)
    tag_bg = models.CharField(max_length=265, null=True, blank=True)
    tag_km = models.CharField(max_length=265, null=True, blank=True)
    tag_ca = models.CharField(max_length=265, null=True, blank=True)
    tag_et = models.CharField(max_length=265, null=True, blank=True)
    tag_gl = models.CharField(max_length=265, null=True, blank=True)
    tag_ka = models.CharField(max_length=265, null=True, blank=True)
    tag_hi = models.CharField(max_length=265, null=True, blank=True)
    tag_hu = models.CharField(max_length=265, null=True, blank=True)
    tag_is = models.CharField(max_length=265, null=True, blank=True)
    tag_id = models.CharField(max_length=265, null=True, blank=True)
    tag_ga = models.CharField(max_length=265, null=True, blank=True)
    tag_mk = models.CharField(max_length=265, null=True, blank=True)
    tag_mn = models.CharField(max_length=265, null=True, blank=True)
    tag_ne = models.CharField(max_length=265, null=True, blank=True)
    tag_ro = models.CharField(max_length=265, null=True, blank=True)
    tag_sr = models.CharField(max_length=265, null=True, blank=True)
    tag_sk = models.CharField(max_length=265, null=True, blank=True)
    tag_ta = models.CharField(max_length=265, null=True, blank=True)
    tag_tg = models.CharField(max_length=265, null=True, blank=True)
    tag_tr = models.CharField(max_length=265, null=True, blank=True)
    tag_ur = models.CharField(max_length=265, null=True, blank=True)
    tag_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "tags"
        verbose_name = "tags"

    def __str__(self):
        return str(self.id) + " - " + str(self.tag) + " - " + str(self.tag_fr)

    def save(self, *args, **kwargs):
        self.tag_fr = language_translate(self.tag_fr, self.tag, "fr")
        self.tag_zh_cn = language_translate(self.tag_zh_cn, self.tag, "zh-cn")
        self.tag_nl = language_translate(self.tag_nl, self.tag, "nl")
        self.tag_de = language_translate(self.tag_de, self.tag, "de")
        self.tag_sw = language_translate(self.tag_sw, self.tag, "sw")
        self.tag_it = language_translate(self.tag_it, self.tag, "it")
        self.tag_ar = language_translate(self.tag_ar, self.tag, "ar")
        self.tag_iw = language_translate(self.tag_iw, self.tag, "iw")
        self.tag_ja = language_translate(self.tag_ja, self.tag, "ja")
        self.tag_ru = language_translate(self.tag_ru, self.tag, "ru")
        self.tag_fa = language_translate(self.tag_fa, self.tag, "fa")
        self.tag_pt_br = language_translate(self.tag_pt_br, self.tag, "pt_br")
        self.tag_pt_pt = language_translate(self.tag_pt_pt, self.tag, "pt_pt")
        self.tag_es = language_translate(self.tag_es, self.tag, "es")
        self.tag_el = language_translate(self.tag_el, self.tag, "el")
        self.tag_zh_tw = language_translate(self.tag_zh_tw, self.tag, "zh-tw")
        self.tag_uk = language_translate(self.tag_uk, self.tag, "uk")
        self.tag_ko = language_translate(self.tag_ko, self.tag, "ko")
        self.tag_pl = language_translate(self.tag_pl, self.tag, "pl")
        self.tag_vi = language_translate(self.tag_vi, self.tag, "vi")
        self.tag_no = language_translate(self.tag_no, self.tag, "no")
        self.tag_sv = language_translate(self.tag_sv, self.tag, "sv")
        self.tag_hr = language_translate(self.tag_hr, self.tag, "hr")
        self.tag_cs = language_translate(self.tag_cs, self.tag, "cs")
        self.tag_da = language_translate(self.tag_da, self.tag, "da")
        self.tag_tl = language_translate(self.tag_tl, self.tag, "tl")
        self.tag_fi = language_translate(self.tag_fi, self.tag, "fi")
        self.tag_sl = language_translate(self.tag_sl, self.tag, "sl")
        self.tag_sq = language_translate(self.tag_sq, self.tag, "sq")
        self.tag_am = language_translate(self.tag_am, self.tag, "am")
        self.tag_hy = language_translate(self.tag_hy, self.tag, "hy")
        self.tag_la = language_translate(self.tag_la, self.tag, "la")
        self.tag_lv = language_translate(self.tag_lv, self.tag, "lv")
        self.tag_th = language_translate(self.tag_th, self.tag, "th")
        self.tag_az = language_translate(self.tag_az, self.tag, "az")
        self.tag_eu = language_translate(self.tag_eu, self.tag, "eu")
        self.tag_be = language_translate(self.tag_be, self.tag, "be")
        self.tag_bn = language_translate(self.tag_bn, self.tag, "bn")
        self.tag_bs = language_translate(self.tag_bs, self.tag, "bs")
        self.tag_bg = language_translate(self.tag_bg, self.tag, "bg")
        self.tag_km = language_translate(self.tag_km, self.tag, "km")
        self.tag_ca = language_translate(self.tag_ca, self.tag, "ca")
        self.tag_et = language_translate(self.tag_et, self.tag, "et")
        self.tag_gl = language_translate(self.tag_gl, self.tag, "gl")
        self.tag_ka = language_translate(self.tag_ka, self.tag, "ka")
        self.tag_hi = language_translate(self.tag_hi, self.tag, "hi")
        self.tag_hu = language_translate(self.tag_hu, self.tag, "hu")
        self.tag_is = language_translate(self.tag_is, self.tag, "is")
        self.tag_id = language_translate(self.tag_id, self.tag, "id")
        self.tag_ga = language_translate(self.tag_ga, self.tag, "ga")
        self.tag_mk = language_translate(self.tag_mk, self.tag, "mk")
        self.tag_mn = language_translate(self.tag_mn, self.tag, "mn")
        self.tag_ne = language_translate(self.tag_ne, self.tag, "ne")
        self.tag_ro = language_translate(self.tag_ro, self.tag, "ro")
        self.tag_sr = language_translate(self.tag_sr, self.tag, "sr")
        self.tag_sk = language_translate(self.tag_sk, self.tag, "sk")
        self.tag_ta = language_translate(self.tag_ta, self.tag, "ta")
        self.tag_tg = language_translate(self.tag_tg, self.tag, "tg")
        self.tag_tr = language_translate(self.tag_tr, self.tag, "tr")
        self.tag_ur = language_translate(self.tag_ur, self.tag, "ur")
        self.tag_uz = language_translate(self.tag_uz, self.tag, "uz")

        return super().save(*args, **kwargs)


class zodiacSign(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    zodiacSign = models.CharField(max_length=265)
    zodiacSign_fr = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_nl = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_de = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sw = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_it = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ar = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_iw = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ja = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ru = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_fa = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_pt_br = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_es = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    zodiacSign_el = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_uk = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ko = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    zodiacSign_pl = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_vi = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    zodiacSign_no = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sv = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_hr = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_cs = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_da = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_tl = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_fi = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sl = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sq = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_am = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_hy = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_la = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_lv = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_th = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_az = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_eu = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_be = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_bn = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_bs = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_bg = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_km = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ca = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_et = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_gl = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ka = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_hi = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_hu = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_is = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_id = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ga = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_mk = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_mn = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ne = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ro = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sr = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_sk = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ta = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_tg = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_tr = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_ur = models.CharField(max_length=265, null=True, blank=True)
    zodiacSign_uz = models.CharField(max_length=265, null=True, blank=True)

    class Meta:
        verbose_name_plural = "zodiacSign"
        verbose_name = "zodiacSign"

    def __str__(self):
        return (
            str(self.id)
            + " - "
            + str(self.zodiacSign)
            + " - "
            + str(self.zodiacSign_fr)
        )

    def save(self, *args, **kwargs):
        self.zodiacSign_fr = language_translate(
            self.zodiacSign_fr, self.zodiacSign, "fr"
        )
        self.zodiacSign_zh_cn = language_translate(
            self.zodiacSign_zh_cn, self.zodiacSign, "zh-cn"
        )
        self.zodiacSign_nl = language_translate(
            self.zodiacSign_nl, self.zodiacSign, "nl"
        )
        self.zodiacSign_de = language_translate(
            self.zodiacSign_de, self.zodiacSign, "de"
        )
        self.zodiacSign_sw = language_translate(
            self.zodiacSign_sw, self.zodiacSign, "sw"
        )
        self.zodiacSign_it = language_translate(
            self.zodiacSign_it, self.zodiacSign, "it"
        )
        self.zodiacSign_ar = language_translate(
            self.zodiacSign_ar, self.zodiacSign, "ar"
        )
        self.zodiacSign_iw = language_translate(
            self.zodiacSign_iw, self.zodiacSign, "iw"
        )
        self.zodiacSign_ja = language_translate(
            self.zodiacSign_ja, self.zodiacSign, "ja"
        )
        self.zodiacSign_ru = language_translate(
            self.zodiacSign_ru, self.zodiacSign, "ru"
        )
        self.zodiacSign_fa = language_translate(
            self.zodiacSign_fa, self.zodiacSign, "fa"
        )
        self.zodiacSign_pt_br = language_translate(
            self.zodiacSign_pt_br, self.zodiacSign, "pt_br"
        )
        self.zodiacSign_pt_pt = language_translate(
            self.zodiacSign_pt_pt, self.zodiacSign, "pt_pt"
        )
        self.zodiacSign_es = language_translate(
            self.zodiacSign_es, self.zodiacSign, "es"
        )
        self.zodiacSign_el = language_translate(
            self.zodiacSign_el, self.zodiacSign, "el"
        )
        self.zodiacSign_zh_tw = language_translate(
            self.zodiacSign_zh_tw, self.zodiacSign, "zh-tw"
        )
        self.zodiacSign_uk = language_translate(
            self.zodiacSign_uk, self.zodiacSign, "uk"
        )
        self.zodiacSign_ko = language_translate(
            self.zodiacSign_ko, self.zodiacSign, "ko"
        )
        self.zodiacSign_pl = language_translate(
            self.zodiacSign_pl, self.zodiacSign, "pl"
        )
        self.zodiacSign_vi = language_translate(
            self.zodiacSign_vi, self.zodiacSign, "vi"
        )
        self.zodiacSign_no = language_translate(
            self.zodiacSign_no, self.zodiacSign, "no"
        )
        self.zodiacSign_sv = language_translate(
            self.zodiacSign_sv, self.zodiacSign, "sv"
        )
        self.zodiacSign_hr = language_translate(
            self.zodiacSign_hr, self.zodiacSign, "hr"
        )
        self.zodiacSign_cs = language_translate(
            self.zodiacSign_cs, self.zodiacSign, "cs"
        )
        self.zodiacSign_da = language_translate(
            self.zodiacSign_da, self.zodiacSign, "da"
        )
        self.zodiacSign_tl = language_translate(
            self.zodiacSign_tl, self.zodiacSign, "tl"
        )
        self.zodiacSign_fi = language_translate(
            self.zodiacSign_fi, self.zodiacSign, "fi"
        )
        self.zodiacSign_sl = language_translate(
            self.zodiacSign_sl, self.zodiacSign, "sl"
        )
        self.zodiacSign_sq = language_translate(
            self.zodiacSign_sq, self.zodiacSign, "sq"
        )
        self.zodiacSign_am = language_translate(
            self.zodiacSign_am, self.zodiacSign, "am"
        )
        self.zodiacSign_hy = language_translate(
            self.zodiacSign_hy, self.zodiacSign, "hy"
        )
        self.zodiacSign_la = language_translate(
            self.zodiacSign_la, self.zodiacSign, "la"
        )
        self.zodiacSign_lv = language_translate(
            self.zodiacSign_lv, self.zodiacSign, "lv"
        )
        self.zodiacSign_th = language_translate(
            self.zodiacSign_th, self.zodiacSign, "th"
        )
        self.zodiacSign_az = language_translate(
            self.zodiacSign_az, self.zodiacSign, "az"
        )
        self.zodiacSign_eu = language_translate(
            self.zodiacSign_eu, self.zodiacSign, "eu"
        )
        self.zodiacSign_be = language_translate(
            self.zodiacSign_be, self.zodiacSign, "be"
        )
        self.zodiacSign_bn = language_translate(
            self.zodiacSign_bn, self.zodiacSign, "bn"
        )
        self.zodiacSign_bs = language_translate(
            self.zodiacSign_bs, self.zodiacSign, "bs"
        )
        self.zodiacSign_bg = language_translate(
            self.zodiacSign_bg, self.zodiacSign, "bg"
        )
        self.zodiacSign_km = language_translate(
            self.zodiacSign_km, self.zodiacSign, "km"
        )
        self.zodiacSign_ca = language_translate(
            self.zodiacSign_ca, self.zodiacSign, "ca"
        )
        self.zodiacSign_et = language_translate(
            self.zodiacSign_et, self.zodiacSign, "et"
        )
        self.zodiacSign_gl = language_translate(
            self.zodiacSign_gl, self.zodiacSign, "gl"
        )
        self.zodiacSign_ka = language_translate(
            self.zodiacSign_ka, self.zodiacSign, "ka"
        )
        self.zodiacSign_hi = language_translate(
            self.zodiacSign_hi, self.zodiacSign, "hi"
        )
        self.zodiacSign_hu = language_translate(
            self.zodiacSign_hu, self.zodiacSign, "hu"
        )
        self.zodiacSign_is = language_translate(
            self.zodiacSign_is, self.zodiacSign, "is"
        )
        self.zodiacSign_id = language_translate(
            self.zodiacSign_id, self.zodiacSign, "id"
        )
        self.zodiacSign_ga = language_translate(
            self.zodiacSign_ga, self.zodiacSign, "ga"
        )
        self.zodiacSign_mk = language_translate(
            self.zodiacSign_mk, self.zodiacSign, "mk"
        )
        self.zodiacSign_mn = language_translate(
            self.zodiacSign_mn, self.zodiacSign, "mn"
        )
        self.zodiacSign_ne = language_translate(
            self.zodiacSign_ne, self.zodiacSign, "ne"
        )
        self.zodiacSign_ro = language_translate(
            self.zodiacSign_ro, self.zodiacSign, "ro"
        )
        self.zodiacSign_sr = language_translate(
            self.zodiacSign_sr, self.zodiacSign, "sr"
        )
        self.zodiacSign_sk = language_translate(
            self.zodiacSign_sk, self.zodiacSign, "sk"
        )
        self.zodiacSign_ta = language_translate(
            self.zodiacSign_ta, self.zodiacSign, "ta"
        )
        self.zodiacSign_tg = language_translate(
            self.zodiacSign_tg, self.zodiacSign, "tg"
        )
        self.zodiacSign_tr = language_translate(
            self.zodiacSign_tr, self.zodiacSign, "tr"
        )
        self.zodiacSign_ur = language_translate(
            self.zodiacSign_ur, self.zodiacSign, "ur"
        )
        self.zodiacSign_uz = language_translate(
            self.zodiacSign_uz, self.zodiacSign, "uz"
        )

        return super().save(*args, **kwargs)


class interestedIn(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "interestedIn"
        verbose_name = "interestedIn"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class config(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)
    coinsPerMessage = models.IntegerField(
        blank=True, null=True, help_text="coins deducted when user sends a message"
    )
    coinsPerPhotoMessage = models.IntegerField(
        blank=True,
        null=True,
        help_text="coins deducted when user sends a photo message",
    )
    coinsPerAvatarPhoto = models.IntegerField(
        default=0, help_text="coins to deduct when user uploads more than 3 photos"
    )

    class Meta:
        verbose_name_plural = "config"
        verbose_name = "config"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class music(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "music"
        verbose_name = "music"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class tvShows(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "tvShows"
        verbose_name = "tvShows"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class sportsTeams(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "sportsTeams"
        verbose_name = "sportsTeams"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class movies(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "movies"
        verbose_name = "movies"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)


class book(models.Model):
    id = models.BigAutoField(primary_key=True)
    interest = models.CharField(max_length=265)
    interest_fr = models.CharField(max_length=265)

    class Meta:
        verbose_name_plural = "book"
        verbose_name = "book"

    def __str__(self):
        return str(self.id) + " - " + str(self.interest) + " - " + str(self.interest_fr)

    def save(self, *args, **kwargs):
        if not self.interest_fr:
            self.interest_fr = translator.translate(
                self.interest, dest="fr"
            ).text.upper()
            time.sleep(0.22)
        return super().save(*args, **kwargs)
