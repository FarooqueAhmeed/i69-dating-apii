from django.db import models
import uuid

from django.dispatch import receiver
from defaultPicker.utils import language_translate_everytime


class Gift(models.Model):
    def get_avatar_path(self, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "static/uploads/gift/" + filename

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    type_choice = (("real", "real_gift"), ("virtual", "virtual_gift"))
    gift_name = models.CharField(max_length=100)
    cost = models.FloatField()
    picture = models.ImageField(upload_to=get_avatar_path, blank=True)
    type = models.CharField(choices=type_choice, max_length=7)

    gift_name_fr = models.CharField(max_length=100)
    gift_name_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_nl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_de = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_it = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ar = models.CharField(max_length=265, null=True, blank=True)
    gift_name_iw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ja = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ru = models.CharField(max_length=265, null=True, blank=True)
    gift_name_fa = models.CharField(max_length=265, null=True, blank=True)
    gift_name_pt_br = models.CharField(max_length=265, null=True, blank=True)
    gift_name_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    gift_name_es = models.CharField(max_length=265, null=True, blank=True)
    gift_name_es_419 = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gift_name_el = models.CharField(max_length=265, null=True, blank=True)
    gift_name_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_uk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ko = models.CharField(max_length=265, null=True, blank=True)
    gift_name_br = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gift_name_pl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_vi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_nn = models.CharField(
        max_length=265, null=True, blank=True
    )  # manually translate due to unavailability in google
    gift_name_no = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sv = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_cs = models.CharField(max_length=265, null=True, blank=True)
    gift_name_da = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_fi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sq = models.CharField(max_length=265, null=True, blank=True)
    gift_name_am = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hy = models.CharField(max_length=265, null=True, blank=True)
    gift_name_la = models.CharField(max_length=265, null=True, blank=True)
    gift_name_lv = models.CharField(max_length=265, null=True, blank=True)
    gift_name_th = models.CharField(max_length=265, null=True, blank=True)
    gift_name_az = models.CharField(max_length=265, null=True, blank=True)
    gift_name_eu = models.CharField(max_length=265, null=True, blank=True)
    gift_name_be = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bs = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bg = models.CharField(max_length=265, null=True, blank=True)
    gift_name_km = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ca = models.CharField(max_length=265, null=True, blank=True)
    gift_name_et = models.CharField(max_length=265, null=True, blank=True)
    gift_name_gl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ka = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hu = models.CharField(max_length=265, null=True, blank=True)
    gift_name_is = models.CharField(max_length=265, null=True, blank=True)
    gift_name_id = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ga = models.CharField(max_length=265, null=True, blank=True)
    gift_name_mk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_mn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ne = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ro = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ta = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tg = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ur = models.CharField(max_length=265, null=True, blank=True)
    gift_name_uz = models.CharField(max_length=265, null=True, blank=True)

    def __str__(self):
        return self.gift_name

    def save(self, *args, **kwargs):
        self.gift_name_fr = language_translate_everytime(
            self.gift_name_fr, self.gift_name, "fr"
        )
        self.gift_name_zh_cn = language_translate_everytime(
            self.gift_name_zh_cn, self.gift_name, "zh-cn"
        )
        self.gift_name_nl = language_translate_everytime(
            self.gift_name_nl, self.gift_name, "nl"
        )
        self.gift_name_de = language_translate_everytime(
            self.gift_name_de, self.gift_name, "de"
        )
        self.gift_name_sw = language_translate_everytime(
            self.gift_name_sw, self.gift_name, "sw"
        )
        self.gift_name_it = language_translate_everytime(
            self.gift_name_it, self.gift_name, "it"
        )
        self.gift_name_ar = language_translate_everytime(
            self.gift_name_ar, self.gift_name, "ar"
        )
        self.gift_name_iw = language_translate_everytime(
            self.gift_name_iw, self.gift_name, "iw"
        )
        self.gift_name_ja = language_translate_everytime(
            self.gift_name_ja, self.gift_name, "ja"
        )
        self.gift_name_ru = language_translate_everytime(
            self.gift_name_ru, self.gift_name, "ru"
        )
        self.gift_name_fa = language_translate_everytime(
            self.gift_name_fa, self.gift_name, "fa"
        )
        self.gift_name_pt_br = language_translate_everytime(
            self.gift_name_pt_br, self.gift_name, "pt_br"
        )
        self.gift_name_pt_pt = language_translate_everytime(
            self.gift_name_pt_pt, self.gift_name, "pt_pt"
        )
        self.gift_name_es = language_translate_everytime(
            self.gift_name_es, self.gift_name, "es"
        )
        self.gift_name_el = language_translate_everytime(
            self.gift_name_el, self.gift_name, "el"
        )
        self.gift_name_zh_tw = language_translate_everytime(
            self.gift_name_zh_tw, self.gift_name, "zh-tw"
        )
        self.gift_name_uk = language_translate_everytime(
            self.gift_name_uk, self.gift_name, "uk"
        )
        self.gift_name_ko = language_translate_everytime(
            self.gift_name_ko, self.gift_name, "ko"
        )
        self.gift_name_pl = language_translate_everytime(
            self.gift_name_pl, self.gift_name, "pl"
        )
        self.gift_name_vi = language_translate_everytime(
            self.gift_name_vi, self.gift_name, "vi"
        )
        self.gift_name_no = language_translate_everytime(
            self.gift_name_no, self.gift_name, "no"
        )
        self.gift_name_sv = language_translate_everytime(
            self.gift_name_sv, self.gift_name, "sv"
        )
        self.gift_name_hr = language_translate_everytime(
            self.gift_name_hr, self.gift_name, "hr"
        )
        self.gift_name_cs = language_translate_everytime(
            self.gift_name_cs, self.gift_name, "cs"
        )
        self.gift_name_da = language_translate_everytime(
            self.gift_name_da, self.gift_name, "da"
        )
        self.gift_name_tl = language_translate_everytime(
            self.gift_name_tl, self.gift_name, "tl"
        )
        self.gift_name_fi = language_translate_everytime(
            self.gift_name_fi, self.gift_name, "fi"
        )
        self.gift_name_sl = language_translate_everytime(
            self.gift_name_sl, self.gift_name, "sl"
        )
        self.gift_name_sq = language_translate_everytime(
            self.gift_name_sq, self.gift_name, "sq"
        )
        self.gift_name_am = language_translate_everytime(
            self.gift_name_am, self.gift_name, "am"
        )
        self.gift_name_hy = language_translate_everytime(
            self.gift_name_hy, self.gift_name, "hy"
        )
        self.gift_name_la = language_translate_everytime(
            self.gift_name_la, self.gift_name, "la"
        )
        self.gift_name_lv = language_translate_everytime(
            self.gift_name_lv, self.gift_name, "lv"
        )
        self.gift_name_th = language_translate_everytime(
            self.gift_name_th, self.gift_name, "th"
        )
        self.gift_name_az = language_translate_everytime(
            self.gift_name_az, self.gift_name, "az"
        )
        self.gift_name_eu = language_translate_everytime(
            self.gift_name_eu, self.gift_name, "eu"
        )
        self.gift_name_be = language_translate_everytime(
            self.gift_name_be, self.gift_name, "be"
        )
        self.gift_name_bn = language_translate_everytime(
            self.gift_name_bn, self.gift_name, "bn"
        )
        self.gift_name_bs = language_translate_everytime(
            self.gift_name_bs, self.gift_name, "bs"
        )
        self.gift_name_bg = language_translate_everytime(
            self.gift_name_bg, self.gift_name, "bg"
        )
        self.gift_name_km = language_translate_everytime(
            self.gift_name_km, self.gift_name, "km"
        )
        self.gift_name_ca = language_translate_everytime(
            self.gift_name_ca, self.gift_name, "ca"
        )
        self.gift_name_et = language_translate_everytime(
            self.gift_name_et, self.gift_name, "et"
        )
        self.gift_name_gl = language_translate_everytime(
            self.gift_name_gl, self.gift_name, "gl"
        )
        self.gift_name_ka = language_translate_everytime(
            self.gift_name_ka, self.gift_name, "ka"
        )
        self.gift_name_hi = language_translate_everytime(
            self.gift_name_hi, self.gift_name, "hi"
        )
        self.gift_name_hu = language_translate_everytime(
            self.gift_name_hu, self.gift_name, "hu"
        )
        self.gift_name_is = language_translate_everytime(
            self.gift_name_is, self.gift_name, "is"
        )
        self.gift_name_id = language_translate_everytime(
            self.gift_name_id, self.gift_name, "id"
        )
        self.gift_name_ga = language_translate_everytime(
            self.gift_name_ga, self.gift_name, "ga"
        )
        self.gift_name_mk = language_translate_everytime(
            self.gift_name_mk, self.gift_name, "mk"
        )
        self.gift_name_mn = language_translate_everytime(
            self.gift_name_mn, self.gift_name, "mn"
        )
        self.gift_name_ne = language_translate_everytime(
            self.gift_name_ne, self.gift_name, "ne"
        )
        self.gift_name_ro = language_translate_everytime(
            self.gift_name_ro, self.gift_name, "ro"
        )
        self.gift_name_sr = language_translate_everytime(
            self.gift_name_sr, self.gift_name, "sr"
        )
        self.gift_name_sk = language_translate_everytime(
            self.gift_name_sk, self.gift_name, "sk"
        )
        self.gift_name_ta = language_translate_everytime(
            self.gift_name_ta, self.gift_name, "ta"
        )
        self.gift_name_tg = language_translate_everytime(
            self.gift_name_tg, self.gift_name, "tg"
        )
        self.gift_name_tr = language_translate_everytime(
            self.gift_name_tr, self.gift_name, "tr"
        )
        self.gift_name_ur = language_translate_everytime(
            self.gift_name_ur, self.gift_name, "ur"
        )
        self.gift_name_uz = language_translate_everytime(
            self.gift_name_uz, self.gift_name, "uz"
        )

        return super().save(*args, **kwargs)


class AllGifts(models.Model):
    type = models.CharField(
        choices=(
            ("real", "real"),
            ("virtual", "virtual"),
        ),
        default="real",
        max_length=50,
    )

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return "%s gift"%self.type

class Giftpurchase(models.Model):
    user = models.ForeignKey(
        'user.User',
        verbose_name="Buyer",
        related_name="user_for_giftpurchase",
        on_delete=models.CASCADE,
    )
    gift = models.ForeignKey(
        AllGifts, related_name="gift_for_giftpurchase", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        'user.User',
        related_name="receiver_for_giftpurchase",
        on_delete=models.CASCADE,
        null=True,
    )
    purchased_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"id:{self.id} {self.gift} {self.user} for {self.receiver} on {self.purchased_on}"


class GiftPurchaseMessageText(models.Model):
    text = models.CharField(max_length=5000)

    def generate_text(self, gift_name, coins):
        custom_text = self.text

        custom_text = custom_text.replace("{1}", gift_name.lower())
        custom_text = custom_text.replace("{2}", str(coins))

        return custom_text

    def __str__(self):
        return self.text


class AbstractGift(models.Model):
    def get_avatar_path(self, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "static/uploads/gift/" + filename

    gift_name = models.CharField(max_length=100)
    cost = models.FloatField()
    picture = models.ImageField(upload_to=get_avatar_path, blank=True)
    allgift = models.OneToOneField(
        AllGifts, on_delete=models.CASCADE, null=True, blank=True
    )

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    gift_name_fr = models.CharField(max_length=100, null=True, blank=True)
    gift_name_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_nl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_de = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_it = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ar = models.CharField(max_length=265, null=True, blank=True)
    gift_name_iw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ja = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ru = models.CharField(max_length=265, null=True, blank=True)
    gift_name_fa = models.CharField(max_length=265, null=True, blank=True)
    gift_name_pt_br = models.CharField(max_length=265, null=True, blank=True)
    gift_name_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    gift_name_es = models.CharField(max_length=265, null=True, blank=True)
    gift_name_el = models.CharField(max_length=265, null=True, blank=True)
    gift_name_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    gift_name_uk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ko = models.CharField(max_length=265, null=True, blank=True)
    gift_name_pl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_vi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_no = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sv = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_cs = models.CharField(max_length=265, null=True, blank=True)
    gift_name_da = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_fi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sq = models.CharField(max_length=265, null=True, blank=True)
    gift_name_am = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hy = models.CharField(max_length=265, null=True, blank=True)
    gift_name_la = models.CharField(max_length=265, null=True, blank=True)
    gift_name_lv = models.CharField(max_length=265, null=True, blank=True)
    gift_name_th = models.CharField(max_length=265, null=True, blank=True)
    gift_name_az = models.CharField(max_length=265, null=True, blank=True)
    gift_name_eu = models.CharField(max_length=265, null=True, blank=True)
    gift_name_be = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bs = models.CharField(max_length=265, null=True, blank=True)
    gift_name_bg = models.CharField(max_length=265, null=True, blank=True)
    gift_name_km = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ca = models.CharField(max_length=265, null=True, blank=True)
    gift_name_et = models.CharField(max_length=265, null=True, blank=True)
    gift_name_gl = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ka = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hi = models.CharField(max_length=265, null=True, blank=True)
    gift_name_hu = models.CharField(max_length=265, null=True, blank=True)
    gift_name_is = models.CharField(max_length=265, null=True, blank=True)
    gift_name_id = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ga = models.CharField(max_length=265, null=True, blank=True)
    gift_name_mk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_mn = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ne = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ro = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_sk = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ta = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tg = models.CharField(max_length=265, null=True, blank=True)
    gift_name_tr = models.CharField(max_length=265, null=True, blank=True)
    gift_name_ur = models.CharField(max_length=265, null=True, blank=True)
    gift_name_uz = models.CharField(max_length=265, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.gift_name

    def save(self, *args, **kwargs):
        self.gift_name_fr = language_translate_everytime(
            self.gift_name_fr, self.gift_name, "fr"
        )
        self.gift_name_zh_cn = language_translate_everytime(
            self.gift_name_zh_cn, self.gift_name, "zh-cn"
        )
        self.gift_name_nl = language_translate_everytime(
            self.gift_name_nl, self.gift_name, "nl"
        )
        self.gift_name_de = language_translate_everytime(
            self.gift_name_de, self.gift_name, "de"
        )
        self.gift_name_sw = language_translate_everytime(
            self.gift_name_sw, self.gift_name, "sw"
        )
        self.gift_name_it = language_translate_everytime(
            self.gift_name_it, self.gift_name, "it"
        )
        self.gift_name_ar = language_translate_everytime(
            self.gift_name_ar, self.gift_name, "ar"
        )
        self.gift_name_iw = language_translate_everytime(
            self.gift_name_iw, self.gift_name, "iw"
        )
        self.gift_name_ja = language_translate_everytime(
            self.gift_name_ja, self.gift_name, "ja"
        )
        self.gift_name_ru = language_translate_everytime(
            self.gift_name_ru, self.gift_name, "ru"
        )
        self.gift_name_fa = language_translate_everytime(
            self.gift_name_fa, self.gift_name, "fa"
        )
        self.gift_name_pt_br = language_translate_everytime(
            self.gift_name_pt_br, self.gift_name, "pt_br"
        )
        self.gift_name_pt_pt = language_translate_everytime(
            self.gift_name_pt_pt, self.gift_name, "pt_pt"
        )
        self.gift_name_es = language_translate_everytime(
            self.gift_name_es, self.gift_name, "es"
        )
        self.gift_name_el = language_translate_everytime(
            self.gift_name_el, self.gift_name, "el"
        )
        self.gift_name_zh_tw = language_translate_everytime(
            self.gift_name_zh_tw, self.gift_name, "zh-tw"
        )
        self.gift_name_uk = language_translate_everytime(
            self.gift_name_uk, self.gift_name, "uk"
        )
        self.gift_name_ko = language_translate_everytime(
            self.gift_name_ko, self.gift_name, "ko"
        )
        self.gift_name_pl = language_translate_everytime(
            self.gift_name_pl, self.gift_name, "pl"
        )
        self.gift_name_vi = language_translate_everytime(
            self.gift_name_vi, self.gift_name, "vi"
        )
        self.gift_name_no = language_translate_everytime(
            self.gift_name_no, self.gift_name, "no"
        )
        self.gift_name_sv = language_translate_everytime(
            self.gift_name_sv, self.gift_name, "sv"
        )
        self.gift_name_hr = language_translate_everytime(
            self.gift_name_hr, self.gift_name, "hr"
        )
        self.gift_name_cs = language_translate_everytime(
            self.gift_name_cs, self.gift_name, "cs"
        )
        self.gift_name_da = language_translate_everytime(
            self.gift_name_da, self.gift_name, "da"
        )
        self.gift_name_tl = language_translate_everytime(
            self.gift_name_tl, self.gift_name, "tl"
        )
        self.gift_name_fi = language_translate_everytime(
            self.gift_name_fi, self.gift_name, "fi"
        )
        self.gift_name_sl = language_translate_everytime(
            self.gift_name_sl, self.gift_name, "sl"
        )
        self.gift_name_sq = language_translate_everytime(
            self.gift_name_sq, self.gift_name, "sq"
        )
        self.gift_name_am = language_translate_everytime(
            self.gift_name_am, self.gift_name, "am"
        )
        self.gift_name_hy = language_translate_everytime(
            self.gift_name_hy, self.gift_name, "hy"
        )
        self.gift_name_la = language_translate_everytime(
            self.gift_name_la, self.gift_name, "la"
        )
        self.gift_name_lv = language_translate_everytime(
            self.gift_name_lv, self.gift_name, "lv"
        )
        self.gift_name_th = language_translate_everytime(
            self.gift_name_th, self.gift_name, "th"
        )
        self.gift_name_az = language_translate_everytime(
            self.gift_name_az, self.gift_name, "az"
        )
        self.gift_name_eu = language_translate_everytime(
            self.gift_name_eu, self.gift_name, "eu"
        )
        self.gift_name_be = language_translate_everytime(
            self.gift_name_be, self.gift_name, "be"
        )
        self.gift_name_bn = language_translate_everytime(
            self.gift_name_bn, self.gift_name, "bn"
        )
        self.gift_name_bs = language_translate_everytime(
            self.gift_name_bs, self.gift_name, "bs"
        )
        self.gift_name_bg = language_translate_everytime(
            self.gift_name_bg, self.gift_name, "bg"
        )
        self.gift_name_km = language_translate_everytime(
            self.gift_name_km, self.gift_name, "km"
        )
        self.gift_name_ca = language_translate_everytime(
            self.gift_name_ca, self.gift_name, "ca"
        )
        self.gift_name_et = language_translate_everytime(
            self.gift_name_et, self.gift_name, "et"
        )
        self.gift_name_gl = language_translate_everytime(
            self.gift_name_gl, self.gift_name, "gl"
        )
        self.gift_name_ka = language_translate_everytime(
            self.gift_name_ka, self.gift_name, "ka"
        )
        self.gift_name_hi = language_translate_everytime(
            self.gift_name_hi, self.gift_name, "hi"
        )
        self.gift_name_hu = language_translate_everytime(
            self.gift_name_hu, self.gift_name, "hu"
        )
        self.gift_name_is = language_translate_everytime(
            self.gift_name_is, self.gift_name, "is"
        )
        self.gift_name_id = language_translate_everytime(
            self.gift_name_id, self.gift_name, "id"
        )
        self.gift_name_ga = language_translate_everytime(
            self.gift_name_ga, self.gift_name, "ga"
        )
        self.gift_name_mk = language_translate_everytime(
            self.gift_name_mk, self.gift_name, "mk"
        )
        self.gift_name_mn = language_translate_everytime(
            self.gift_name_mn, self.gift_name, "mn"
        )
        self.gift_name_ne = language_translate_everytime(
            self.gift_name_ne, self.gift_name, "ne"
        )
        self.gift_name_ro = language_translate_everytime(
            self.gift_name_ro, self.gift_name, "ro"
        )
        self.gift_name_sr = language_translate_everytime(
            self.gift_name_sr, self.gift_name, "sr"
        )
        self.gift_name_sk = language_translate_everytime(
            self.gift_name_sk, self.gift_name, "sk"
        )
        self.gift_name_ta = language_translate_everytime(
            self.gift_name_ta, self.gift_name, "ta"
        )
        self.gift_name_tg = language_translate_everytime(
            self.gift_name_tg, self.gift_name, "tg"
        )
        self.gift_name_tr = language_translate_everytime(
            self.gift_name_tr, self.gift_name, "tr"
        )
        self.gift_name_ur = language_translate_everytime(
            self.gift_name_ur, self.gift_name, "ur"
        )
        self.gift_name_uz = language_translate_everytime(
            self.gift_name_uz, self.gift_name, "uz"
        )

        return super().save(*args, **kwargs)


class RealGift(AbstractGift):
    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not self.allgift:
            params = {"type": "real"}
            if kwargs.get("status"):
                params["status"] = self.status
            self.allgift = AllGifts.objects.create(**params)
        else:
            self.allgift.status = self.status
            self.allgift.save()

        return result


class VirtualGift(AbstractGift):

    def save(self, *args, **kwargs):

        result = super().save(*args, **kwargs)
        if not self.allgift:
            params = {"type": "virtual"}
            if kwargs.get("status"):
                params["status"] = self.status
            self.allgift = AllGifts.objects.create(**params)
        else:
            self.allgift.status = self.status
            self.allgift.save()

        return result


class RealGiftPriceForRegion(models.Model):
    real_gift = models.ForeignKey(RealGift, on_delete=models.CASCADE)
    region = models.ForeignKey('user.CoinSettingsRegion', on_delete=models.CASCADE)
    cost = models.FloatField()

    def __str__(self):
        return self.real_gift.gift_name + " (" + self.region.title + ")"


class VirtualGiftPriceForRegion(models.Model):
    virtual_gift = models.ForeignKey(VirtualGift, on_delete=models.CASCADE)
    region = models.ForeignKey('user.CoinSettingsRegion', on_delete=models.CASCADE)
    cost = models.FloatField()

    def __str__(self):
        return self.virtual_gift.gift_name + " (" + self.region.title + ")"
