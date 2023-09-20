from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    SET_NULL,
    AutoField,
    BigAutoField,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
    FloatField,
)

from defaultPicker.utils import language_translate, SUPPORTED_LANGUAGES

from .utils import package_plan_duration_choices


class Purchase(Model):
    purchase_id = BigAutoField(primary_key=True, unique=True)
    user = ForeignKey('user.User', on_delete=CASCADE, null=True)
    method = CharField(max_length=255)
    coins = IntegerField()
    money = DecimalField(max_digits=5, decimal_places=2)
    purchased_on = DateTimeField(auto_now_add=True, null=True)
    payment_method = CharField(
        max_length=255, default=None, null=True, blank=True
    )  # choices = payment_method_choices,
    currency = CharField(max_length=100, default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Purchase"
        verbose_name = "Purchase"

    def __str__(self):
        return f"id:{self.purchase_id} {self.coins} coins by {self.user} on {self.purchased_on}"

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)

        # Add Coins to user wallet.
        user = self.user
        user.purchase_coins = user.purchase_coins + self.coins
        user.purchase_coins_date = self.purchased_on
        user.save()

        return obj


class Permission(Model):
    permission_choices = [
        (
            "SHARE_MOMENT",
            "SHARE_MOMENT",
        ),
        (
            "SHARE_USER_LOCATION",
            "SHARE_USER_LOCATION",
        ),
        (
            "REQUEST_USER_PRIVATE_ALBUM_ACCESS",
            "REQUEST_USER_PRIVATE_ALBUM_ACCESS",
        ),
        (
            "SHARE_STORY",
            "SHARE_STORY",
        ),
        (
            "FIRST_FREE_MESSAGE",
            "FIRST_FREE_MESSAGE",
        ),
        (     
            "RANDOM_SEARCHED_USER_RESULTS_LIMIT",
            "RANDOM_SEARCHED_USER_RESULTS_LIMIT",
        ),
        (     
            "POPULAR_SEARCHED_USER_RESULTS_LIMIT",
            "POPULAR_SEARCHED_USER_RESULTS_LIMIT",
        ),
        (     
            "MOST_ACTIVE_SEARCHED_USER_RESULTS_LIMIT",
            "MOST_ACTIVE_SEARCHED_USER_RESULTS_LIMIT",
        ),
        (
            "COMMENT_UNLIMITED_MOMENT",
            "COMMENT_UNLIMITED_MOMENT",
        ),
        (
            "COMMENT_UNLIMITED_STORY",
            "COMMENT_UNLIMITED_STORY",
        ),
        (
            "SEE_WHO_VISITED_YOUR_PROFILE",
            "SEE_WHO_VISITED_YOUR_PROFILE",
        ),
        (
            "BE_NOTIFIED_FIRST_WHEN_THERE_IS_NEW_USER_IN_YOUR_AREA",
            "BE_NOTIFIED_FIRST_WHEN_THERE_IS_NEW_USER_IN_YOUR_AREA",
        ),
        (
            "VIEW_WHO_READ(SEEN)_YOUR_sent_MESSAGE",
            "VIEW_WHO_READ(SEEN)_YOUR_sent_MESSAGE",
        ),
    ]
    id = AutoField(primary_key=True)
    name = CharField(max_length=255, unique=True, null=False, blank=False, choices=permission_choices)
    description = CharField(max_length=255, blank=True, null=True, default=None)
    user_free_limit = IntegerField(default=0, blank=True, verbose_name="User free daily limit")
    user_unlocked_result_limit = IntegerField(default=0, blank=True, verbose_name="User unlocked result daily limit")
    description_fr = CharField(max_length=255, null=True, blank=True)
    description_zh_cn = CharField(max_length=255, null=True, blank=True)
    description_nl = CharField(max_length=255, null=True, blank=True)
    description_de = CharField(max_length=255, null=True, blank=True)
    description_sw = CharField(max_length=255, null=True, blank=True)
    description_it = CharField(max_length=255, null=True, blank=True)
    description_ar = CharField(max_length=255, null=True, blank=True)
    description_iw = CharField(max_length=255, null=True, blank=True)
    description_ja = CharField(max_length=255, null=True, blank=True)
    description_ru = CharField(max_length=255, null=True, blank=True)
    description_fa = CharField(max_length=255, null=True, blank=True)
    description_pt_br = CharField(max_length=255, null=True, blank=True)
    description_pt_pt = CharField(max_length=255, null=True, blank=True)
    description_es = CharField(max_length=255, null=True, blank=True)
    description_es_419 = CharField(max_length=255, null=True, blank=True)
    description_el = CharField(max_length=255, null=True, blank=True)
    description_zh_tw = CharField(max_length=255, null=True, blank=True)
    description_uk = CharField(max_length=255, null=True, blank=True)
    description_ko = CharField(max_length=255, null=True, blank=True)
    description_br = CharField(max_length=255, null=True, blank=True)  # manually translate due to unavailability in google
    description_pl = CharField(max_length=255, null=True, blank=True)
    description_vi = CharField(max_length=255, null=True, blank=True)
    description_nn = CharField(max_length=255, null=True, blank=True)  # manually translate due to unavailability in google
    description_no = CharField(max_length=255, null=True, blank=True)
    description_sv = CharField(max_length=255, null=True, blank=True)
    description_hr = CharField(max_length=255, null=True, blank=True)
    description_cs = CharField(max_length=255, null=True, blank=True)
    description_da = CharField(max_length=255, null=True, blank=True)
    description_tl = CharField(max_length=255, null=True, blank=True)
    description_fi = CharField(max_length=255, null=True, blank=True)
    description_sl = CharField(max_length=255, null=True, blank=True)
    description_sq = CharField(max_length=255, null=True, blank=True)
    description_am = CharField(max_length=255, null=True, blank=True)
    description_hy = CharField(max_length=255, null=True, blank=True)
    description_la = CharField(max_length=255, null=True, blank=True)
    description_lv = CharField(max_length=255, null=True, blank=True)
    description_th = CharField(max_length=255, null=True, blank=True)
    description_az = CharField(max_length=255, null=True, blank=True)
    description_eu = CharField(max_length=255, null=True, blank=True)
    description_be = CharField(max_length=255, null=True, blank=True)
    description_bn = CharField(max_length=255, null=True, blank=True)
    description_bs = CharField(max_length=255, null=True, blank=True)
    description_bg = CharField(max_length=255, null=True, blank=True)
    description_km = CharField(max_length=255, null=True, blank=True)
    description_ca = CharField(max_length=255, null=True, blank=True)
    description_et = CharField(max_length=255, null=True, blank=True)
    description_gl = CharField(max_length=255, null=True, blank=True)
    description_ka = CharField(max_length=255, null=True, blank=True)
    description_hi = CharField(max_length=255, null=True, blank=True)
    description_hu = CharField(max_length=255, null=True, blank=True)
    description_is = CharField(max_length=255, null=True, blank=True)
    description_id = CharField(max_length=255, null=True, blank=True)
    description_ga = CharField(max_length=255, null=True, blank=True)
    description_mk = CharField(max_length=255, null=True, blank=True)
    description_mn = CharField(max_length=255, null=True, blank=True)
    description_ne = CharField(max_length=255, null=True, blank=True)
    description_ro = CharField(max_length=255, null=True, blank=True)
    description_sr = CharField(max_length=255, null=True, blank=True)
    description_sk = CharField(max_length=255, null=True, blank=True)
    description_ta = CharField(max_length=255, null=True, blank=True)
    description_tg = CharField(max_length=255, null=True, blank=True)
    description_tr = CharField(max_length=255, null=True, blank=True)
    description_ur = CharField(max_length=255, null=True, blank=True)
    description_uz = CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        for lang in SUPPORTED_LANGUAGES:
            lang_str = lang
            if "-" in lang_str:
                lang_str = lang_str.replace("-", "_")
            description_field = "description_%s" % lang_str
            setattr(
                self,
                description_field,
                language_translate(getattr(self, description_field), self.description, lang),
            )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Package Service"
        verbose_name_plural = "Package Services"


class Package(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=65)
    name_fr = CharField(max_length=65, null=True, blank=True)
    name_zh_cn = CharField(max_length=65, null=True, blank=True)
    name_nl = CharField(max_length=65, null=True, blank=True)
    name_de = CharField(max_length=65, null=True, blank=True)
    name_sw = CharField(max_length=65, null=True, blank=True)
    name_it = CharField(max_length=65, null=True, blank=True)
    name_ar = CharField(max_length=65, null=True, blank=True)
    name_iw = CharField(max_length=65, null=True, blank=True)
    name_ja = CharField(max_length=65, null=True, blank=True)
    name_ru = CharField(max_length=65, null=True, blank=True)
    name_fa = CharField(max_length=65, null=True, blank=True)
    name_pt_br = CharField(max_length=65, null=True, blank=True)
    name_pt_pt = CharField(max_length=65, null=True, blank=True)
    name_es = CharField(max_length=65, null=True, blank=True)
    name_es_419 = CharField(
        max_length=65, null=True, blank=True
    )  # manually translate due to unavailability in google
    name_el = CharField(max_length=65, null=True, blank=True)
    name_zh_tw = CharField(max_length=65, null=True, blank=True)
    name_uk = CharField(max_length=65, null=True, blank=True)
    name_ko = CharField(max_length=65, null=True, blank=True)
    name_br = CharField(
        max_length=65, null=True, blank=True
    )  # manually translate due to unavailability in google
    name_pl = CharField(max_length=65, null=True, blank=True)
    name_vi = CharField(max_length=65, null=True, blank=True)
    name_nn = CharField(
        max_length=65, null=True, blank=True
    )  # manually translate due to unavailability in google
    name_no = CharField(max_length=65, null=True, blank=True)
    name_sv = CharField(max_length=65, null=True, blank=True)
    name_hr = CharField(max_length=65, null=True, blank=True)
    name_cs = CharField(max_length=65, null=True, blank=True)
    name_da = CharField(max_length=65, null=True, blank=True)
    name_tl = CharField(max_length=65, null=True, blank=True)
    name_fi = CharField(max_length=65, null=True, blank=True)
    name_sl = CharField(max_length=65, null=True, blank=True)
    name_sq = CharField(max_length=65, null=True, blank=True)
    name_am = CharField(max_length=65, null=True, blank=True)
    name_hy = CharField(max_length=65, null=True, blank=True)
    name_la = CharField(max_length=65, null=True, blank=True)
    name_lv = CharField(max_length=65, null=True, blank=True)
    name_th = CharField(max_length=65, null=True, blank=True)
    name_az = CharField(max_length=65, null=True, blank=True)
    name_eu = CharField(max_length=65, null=True, blank=True)
    name_be = CharField(max_length=65, null=True, blank=True)
    name_bn = CharField(max_length=65, null=True, blank=True)
    name_bs = CharField(max_length=65, null=True, blank=True)
    name_bg = CharField(max_length=65, null=True, blank=True)
    name_km = CharField(max_length=65, null=True, blank=True)
    name_ca = CharField(max_length=65, null=True, blank=True)
    name_et = CharField(max_length=65, null=True, blank=True)
    name_gl = CharField(max_length=65, null=True, blank=True)
    name_ka = CharField(max_length=65, null=True, blank=True)
    name_hi = CharField(max_length=65, null=True, blank=True)
    name_hu = CharField(max_length=65, null=True, blank=True)
    name_is = CharField(max_length=65, null=True, blank=True)
    name_id = CharField(max_length=65, null=True, blank=True)
    name_ga = CharField(max_length=65, null=True, blank=True)
    name_mk = CharField(max_length=65, null=True, blank=True)
    name_mn = CharField(max_length=65, null=True, blank=True)
    name_ne = CharField(max_length=65, null=True, blank=True)
    name_ro = CharField(max_length=65, null=True, blank=True)
    name_sr = CharField(max_length=65, null=True, blank=True)
    name_sk = CharField(max_length=65, null=True, blank=True)
    name_ta = CharField(max_length=65, null=True, blank=True)
    name_tg = CharField(max_length=65, null=True, blank=True)
    name_tr = CharField(max_length=65, null=True, blank=True)
    name_ur = CharField(max_length=65, null=True, blank=True)
    name_uz = CharField(max_length=65, null=True, blank=True)
    description = TextField()
    permissions = ManyToManyField(Permission, blank=True, verbose_name="Services")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_fr = language_translate(self.name_fr, self.name, "fr")
        self.name_zh_cn = language_translate(self.name_zh_cn, self.name, "zh-cn")
        self.name_nl = language_translate(self.name_nl, self.name, "nl")
        self.name_de = language_translate(self.name_de, self.name, "de")
        self.name_sw = language_translate(self.name_sw, self.name, "sw")
        self.name_it = language_translate(self.name_it, self.name, "it")
        self.name_ar = language_translate(self.name_ar, self.name, "ar")
        self.name_iw = language_translate(self.name_iw, self.name, "iw")
        self.name_ja = language_translate(self.name_ja, self.name, "ja")
        self.name_ru = language_translate(self.name_ru, self.name, "ru")
        self.name_fa = language_translate(self.name_fa, self.name, "fa")
        self.name_pt_br = language_translate(self.name_pt_br, self.name, "pt_br")
        self.name_pt_pt = language_translate(self.name_pt_pt, self.name, "pt_pt")
        self.name_es = language_translate(self.name_es, self.name, "es")
        self.name_el = language_translate(self.name_el, self.name, "el")
        self.name_zh_tw = language_translate(self.name_zh_tw, self.name, "zh-tw")
        self.name_uk = language_translate(self.name_uk, self.name, "uk")
        self.name_ko = language_translate(self.name_ko, self.name, "ko")
        self.name_pl = language_translate(self.name_pl, self.name, "pl")
        self.name_vi = language_translate(self.name_vi, self.name, "vi")
        self.name_no = language_translate(self.name_no, self.name, "no")
        self.name_sv = language_translate(self.name_sv, self.name, "sv")
        self.name_hr = language_translate(self.name_hr, self.name, "hr")
        self.name_cs = language_translate(self.name_cs, self.name, "cs")
        self.name_da = language_translate(self.name_da, self.name, "da")
        self.name_tl = language_translate(self.name_tl, self.name, "tl")
        self.name_fi = language_translate(self.name_fi, self.name, "fi")
        self.name_sl = language_translate(self.name_sl, self.name, "sl")
        self.name_sq = language_translate(self.name_sq, self.name, "sq")
        self.name_am = language_translate(self.name_am, self.name, "am")
        self.name_hy = language_translate(self.name_hy, self.name, "hy")
        self.name_la = language_translate(self.name_la, self.name, "la")
        self.name_lv = language_translate(self.name_lv, self.name, "lv")
        self.name_th = language_translate(self.name_th, self.name, "th")
        self.name_az = language_translate(self.name_az, self.name, "az")
        self.name_eu = language_translate(self.name_eu, self.name, "eu")
        self.name_be = language_translate(self.name_be, self.name, "be")
        self.name_bn = language_translate(self.name_bn, self.name, "bn")
        self.name_bs = language_translate(self.name_bs, self.name, "bs")
        self.name_bg = language_translate(self.name_bg, self.name, "bg")
        self.name_km = language_translate(self.name_km, self.name, "km")
        self.name_ca = language_translate(self.name_ca, self.name, "ca")
        self.name_et = language_translate(self.name_et, self.name, "et")
        self.name_gl = language_translate(self.name_gl, self.name, "gl")
        self.name_ka = language_translate(self.name_ka, self.name, "ka")
        self.name_hi = language_translate(self.name_hi, self.name, "hi")
        self.name_hu = language_translate(self.name_hu, self.name, "hu")
        self.name_is = language_translate(self.name_is, self.name, "is")
        self.name_id = language_translate(self.name_id, self.name, "id")
        self.name_ga = language_translate(self.name_ga, self.name, "ga")
        self.name_mk = language_translate(self.name_mk, self.name, "mk")
        self.name_mn = language_translate(self.name_mn, self.name, "mn")
        self.name_ne = language_translate(self.name_ne, self.name, "ne")
        self.name_ro = language_translate(self.name_ro, self.name, "ro")
        self.name_sr = language_translate(self.name_sr, self.name, "sr")
        self.name_sk = language_translate(self.name_sk, self.name, "sk")
        self.name_ta = language_translate(self.name_ta, self.name, "ta")
        self.name_tg = language_translate(self.name_tg, self.name, "tg")
        self.name_tr = language_translate(self.name_tr, self.name, "tr")
        self.name_ur = language_translate(self.name_ur, self.name, "ur")
        self.name_uz = language_translate(self.name_uz, self.name, "uz")

        return super().save(*args, **kwargs)


class Plan(Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=255, null=True, blank=True)
    title_fr = CharField(max_length=255, null=True, blank=True)
    title_zh_cn = CharField(max_length=255, null=True, blank=True)
    title_nl = CharField(max_length=255, null=True, blank=True)
    title_de = CharField(max_length=255, null=True, blank=True)
    title_sw = CharField(max_length=255, null=True, blank=True)
    title_it = CharField(max_length=255, null=True, blank=True)
    title_ar = CharField(max_length=255, null=True, blank=True)
    title_iw = CharField(max_length=255, null=True, blank=True)
    title_ja = CharField(max_length=255, null=True, blank=True)
    title_ru = CharField(max_length=255, null=True, blank=True)
    title_fa = CharField(max_length=255, null=True, blank=True)
    title_pt_br = CharField(max_length=255, null=True, blank=True)
    title_pt_pt = CharField(max_length=255, null=True, blank=True)
    title_es = CharField(max_length=255, null=True, blank=True)
    title_es_419 = CharField(
        max_length=255, null=True, blank=True
    )  # manually translate due to unavailability in google
    title_el = CharField(max_length=255, null=True, blank=True)
    title_zh_tw = CharField(max_length=255, null=True, blank=True)
    title_uk = CharField(max_length=255, null=True, blank=True)
    title_ko = CharField(max_length=255, null=True, blank=True)
    title_br = CharField(
        max_length=255, null=True, blank=True
    )  # manually translate due to unavailability in google
    title_pl = CharField(max_length=255, null=True, blank=True)
    title_vi = CharField(max_length=255, null=True, blank=True)
    title_nn = CharField(
        max_length=255, null=True, blank=True
    )  # manually translate due to unavailability in google
    title_no = CharField(max_length=255, null=True, blank=True)
    title_sv = CharField(max_length=255, null=True, blank=True)
    title_hr = CharField(max_length=255, null=True, blank=True)
    title_cs = CharField(max_length=255, null=True, blank=True)
    title_da = CharField(max_length=255, null=True, blank=True)
    title_tl = CharField(max_length=255, null=True, blank=True)
    title_fi = CharField(max_length=255, null=True, blank=True)
    title_sl = CharField(max_length=255, null=True, blank=True)
    title_sq = CharField(max_length=255, null=True, blank=True)
    title_am = CharField(max_length=255, null=True, blank=True)
    title_hy = CharField(max_length=255, null=True, blank=True)
    title_la = CharField(max_length=255, null=True, blank=True)
    title_lv = CharField(max_length=255, null=True, blank=True)
    title_th = CharField(max_length=255, null=True, blank=True)
    title_az = CharField(max_length=255, null=True, blank=True)
    title_eu = CharField(max_length=255, null=True, blank=True)
    title_be = CharField(max_length=255, null=True, blank=True)
    title_bn = CharField(max_length=255, null=True, blank=True)
    title_bs = CharField(max_length=255, null=True, blank=True)
    title_bg = CharField(max_length=255, null=True, blank=True)
    title_km = CharField(max_length=255, null=True, blank=True)
    title_ca = CharField(max_length=255, null=True, blank=True)
    title_et = CharField(max_length=255, null=True, blank=True)
    title_gl = CharField(max_length=255, null=True, blank=True)
    title_ka = CharField(max_length=255, null=True, blank=True)
    title_hi = CharField(max_length=255, null=True, blank=True)
    title_hu = CharField(max_length=255, null=True, blank=True)
    title_is = CharField(max_length=255, null=True, blank=True)
    title_id = CharField(max_length=255, null=True, blank=True)
    title_ga = CharField(max_length=255, null=True, blank=True)
    title_mk = CharField(max_length=255, null=True, blank=True)
    title_mn = CharField(max_length=255, null=True, blank=True)
    title_ne = CharField(max_length=255, null=True, blank=True)
    title_ro = CharField(max_length=255, null=True, blank=True)
    title_sr = CharField(max_length=255, null=True, blank=True)
    title_sk = CharField(max_length=255, null=True, blank=True)
    title_ta = CharField(max_length=255, null=True, blank=True)
    title_tg = CharField(max_length=255, null=True, blank=True)
    title_tr = CharField(max_length=255, null=True, blank=True)
    title_ur = CharField(max_length=255, null=True, blank=True)
    title_uz = CharField(max_length=255, null=True, blank=True)
    price_in_coins = IntegerField(verbose_name="Coins", default=0)
    is_on_discount = BooleanField(default=False)
    is_active = BooleanField(default=True)
    validity = CharField(
        choices=package_plan_duration_choices, default="PERMONTH", max_length=100
    )
    dicounted_price_in_coins = IntegerField(default=0, null=True, blank=True)
    package = ForeignKey(Package, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_fr = language_translate(self.title_fr, self.title, "fr")
        self.title_zh_cn = language_translate(self.title_zh_cn, self.title, "zh-cn")
        self.title_nl = language_translate(self.title_nl, self.title, "nl")
        self.title_de = language_translate(self.title_de, self.title, "de")
        self.title_sw = language_translate(self.title_sw, self.title, "sw")
        self.title_it = language_translate(self.title_it, self.title, "it")
        self.title_ar = language_translate(self.title_ar, self.title, "ar")
        self.title_iw = language_translate(self.title_iw, self.title, "iw")
        self.title_ja = language_translate(self.title_ja, self.title, "ja")
        self.title_ru = language_translate(self.title_ru, self.title, "ru")
        self.title_fa = language_translate(self.title_fa, self.title, "fa")
        self.title_pt_br = language_translate(self.title_pt_br, self.title, "pt_br")
        self.title_pt_pt = language_translate(self.title_pt_pt, self.title, "pt_pt")
        self.title_es = language_translate(self.title_es, self.title, "es")
        self.title_el = language_translate(self.title_el, self.title, "el")
        self.title_zh_tw = language_translate(self.title_zh_tw, self.title, "zh-tw")
        self.title_uk = language_translate(self.title_uk, self.title, "uk")
        self.title_ko = language_translate(self.title_ko, self.title, "ko")
        self.title_pl = language_translate(self.title_pl, self.title, "pl")
        self.title_vi = language_translate(self.title_vi, self.title, "vi")
        self.title_no = language_translate(self.title_no, self.title, "no")
        self.title_sv = language_translate(self.title_sv, self.title, "sv")
        self.title_hr = language_translate(self.title_hr, self.title, "hr")
        self.title_cs = language_translate(self.title_cs, self.title, "cs")
        self.title_da = language_translate(self.title_da, self.title, "da")
        self.title_tl = language_translate(self.title_tl, self.title, "tl")
        self.title_fi = language_translate(self.title_fi, self.title, "fi")
        self.title_sl = language_translate(self.title_sl, self.title, "sl")
        self.title_sq = language_translate(self.title_sq, self.title, "sq")
        self.title_am = language_translate(self.title_am, self.title, "am")
        self.title_hy = language_translate(self.title_hy, self.title, "hy")
        self.title_la = language_translate(self.title_la, self.title, "la")
        self.title_lv = language_translate(self.title_lv, self.title, "lv")
        self.title_th = language_translate(self.title_th, self.title, "th")
        self.title_az = language_translate(self.title_az, self.title, "az")
        self.title_eu = language_translate(self.title_eu, self.title, "eu")
        self.title_be = language_translate(self.title_be, self.title, "be")
        self.title_bn = language_translate(self.title_bn, self.title, "bn")
        self.title_bs = language_translate(self.title_bs, self.title, "bs")
        self.title_bg = language_translate(self.title_bg, self.title, "bg")
        self.title_km = language_translate(self.title_km, self.title, "km")
        self.title_ca = language_translate(self.title_ca, self.title, "ca")
        self.title_et = language_translate(self.title_et, self.title, "et")
        self.title_gl = language_translate(self.title_gl, self.title, "gl")
        self.title_ka = language_translate(self.title_ka, self.title, "ka")
        self.title_hi = language_translate(self.title_hi, self.title, "hi")
        self.title_hu = language_translate(self.title_hu, self.title, "hu")
        self.title_is = language_translate(self.title_is, self.title, "is")
        self.title_id = language_translate(self.title_id, self.title, "id")
        self.title_ga = language_translate(self.title_ga, self.title, "ga")
        self.title_mk = language_translate(self.title_mk, self.title, "mk")
        self.title_mn = language_translate(self.title_mn, self.title, "mn")
        self.title_ne = language_translate(self.title_ne, self.title, "ne")
        self.title_ro = language_translate(self.title_ro, self.title, "ro")
        self.title_sr = language_translate(self.title_sr, self.title, "sr")
        self.title_sk = language_translate(self.title_sk, self.title, "sk")
        self.title_ta = language_translate(self.title_ta, self.title, "ta")
        self.title_tg = language_translate(self.title_tg, self.title, "tg")
        self.title_tr = language_translate(self.title_tr, self.title, "tr")
        self.title_ur = language_translate(self.title_ur, self.title, "ur")
        self.title_uz = language_translate(self.title_uz, self.title, "uz")

        return super().save(*args, **kwargs)


class PackagePurchase(Model):
    package = ForeignKey(Package, on_delete=CASCADE, related_name="purchases")
    plan = ForeignKey(
        Plan,
        on_delete=CASCADE,
        related_name="plan",
        null=True,
        blank=True,
        default=None,
    )
    user = ForeignKey('user.User', on_delete=SET_NULL, null=True, related_name="packages")
    is_active = BooleanField(default=False)
    starts_at = DateTimeField(null=False, blank=False, default=None)
    ends_at = DateTimeField(null=False, blank=False, default=None)
    package_price = IntegerField(null=True, blank=True, default=None)
    purchase_price = IntegerField(null=True, blank=True, default=None)
    renewed_at = DateTimeField(null=True, blank=True, default=None)
    renewed_subscription = ForeignKey(
        "PackagePurchase",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="renewed_package",
    )
    downgraded_at = DateTimeField(null=True, blank=True, default=None)
    upgraded_at = DateTimeField(null=True, blank=True, default=None)
    downgraded_to_package = ForeignKey(
        Package,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="downgraded_package",
    )
    upgraded_to_package = ForeignKey(
        Package,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="upgraded_package",
    )

    cancelled_at = DateTimeField(null=True, blank=True, default=None)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by_admin = BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return str(self.package) + " | Package for user: " + str(self.user)

    def clean(self):
        user = self.user
        already_purchased = False
        if self.is_active:
            already_purchased = PackagePurchase.objects.filter(
                user=user, is_active=True
            )
            if self.id:
                already_purchased = already_purchased.exclude(id=self.id)
            already_purchased = already_purchased.first()
        if already_purchased:
            raise ValidationError("Active package already found for this user.")

    class Meta:
        verbose_name = "Package Purchase"
        verbose_name_plural = "Package Purchases"


class PackagePermissionLimit(Model):
    id = AutoField(primary_key=True)
    package = ForeignKey(Package, on_delete=CASCADE, related_name="package")
    permission = ForeignKey(
        Permission, on_delete=CASCADE, related_name="permission", verbose_name="Service"
    )
    per_day = IntegerField(default=0)
    per_week = IntegerField(default=0)
    per_month = IntegerField(default=0)
    is_unlimited = BooleanField(default=False)

    def clean(self):
        package = self.package
        permission = self.permission
        already_added = False
        already_added = PackagePermissionLimit.objects.filter(
            package=package, permission=permission
        )
        if self.id:
            already_added = already_added.exclude(id=self.id)
        already_added = already_added.first()
        if already_added:
            raise ValidationError("Limit is already exist for this package.")

    class Meta:
        verbose_name = "Package Service Limit"
        verbose_name_plural = "Package Service Limits"


"""
    This model contains the dynamic prices of coins
"""


class CoinPrices(Model):
    coins_count = IntegerField(default=0)
    original_price = FloatField()
    discounted_price = FloatField()
    is_active = BooleanField(default=True)
    currency = CharField(max_length=50, default="EUR")

    def __str__(self):
        return str(self.coins_count)

    class Meta:
        verbose_name = "Coin Prices"
        verbose_name_plural = "Coin Prices"


class CoinPricesForRegion(Model):
    coin_price = ForeignKey(CoinPrices, on_delete=CASCADE)
    region = ForeignKey('user.CoinSettingsRegion', on_delete=CASCADE)
    coins_count = IntegerField(default=0)
    original_price = FloatField()
    discounted_price = FloatField()

    def __str__(self):
        return str(self.coins_count) + " (" + self.region.title + ")"


class PlanForRegion(Model):
    plan = ForeignKey(Plan, on_delete=CASCADE)
    region = ForeignKey('user.CoinSettingsRegion', on_delete=CASCADE)
    price_in_coins = IntegerField(verbose_name="Coins", default=0)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.plan.title + " (" + self.region.title + ")"
