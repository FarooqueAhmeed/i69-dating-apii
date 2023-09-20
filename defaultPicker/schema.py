from django.db import models
import graphene
from graphene import *
from .models import (
    age,
    ethnicity,
    politics,
    religious,
    Language,
    family,
    zodiacSign,
    tags,
    interestedIn,
    gender,
    height,
    searchGender,
    config,
)
from django.db.models import F

from defaultPicker.utils import translated_field_name, custom_translate


class DefaultObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()
    value_zh_cn = graphene.String()
    value_nl = graphene.String()
    value_de = graphene.String()
    value_sw = graphene.String()
    value_it = graphene.String()
    value_ar = graphene.String()
    value_iw = graphene.String()
    value_ja = graphene.String()
    value_ru = graphene.String()
    value_fa = graphene.String()
    value_pt_br = graphene.String()
    value_pt_pt = graphene.String()
    value_es = graphene.String()
    value_es_419 = graphene.String()
    value_el = graphene.String()
    value_zh_tw = graphene.String()
    value_uk = graphene.String()
    value_ko = graphene.String()
    value_br = graphene.String()
    value_pl = graphene.String()
    value_vi = graphene.String()
    value_nn = graphene.String()
    value_no = graphene.String()
    value_sv = graphene.String()
    value_hr = graphene.String()
    value_cs = graphene.String()
    value_da = graphene.String()
    value_tl = graphene.String()
    value_fi = graphene.String()
    value_sl = graphene.String()
    value_sq = graphene.String()
    value_am = graphene.String()
    value_hy = graphene.String()
    value_la = graphene.String()
    value_lv = graphene.String()
    value_th = graphene.String()
    value_az = graphene.String()
    value_eu = graphene.String()
    value_be = graphene.String()
    value_bn = graphene.String()
    value_bs = graphene.String()
    value_bg = graphene.String()
    value_km = graphene.String()
    value_ca = graphene.String()
    value_et = graphene.String()
    value_gl = graphene.String()
    value_ka = graphene.String()
    value_hi = graphene.String()
    value_hu = graphene.String()
    value_i = graphene.String()
    value_i = graphene.String()
    value_g = graphene.String()
    value_m = graphene.String()
    value_m = graphene.String()
    value_n = graphene.String()
    value_r = graphene.String()
    value_s = graphene.String()
    value_s = graphene.String()
    value_t = graphene.String()
    value_t = graphene.String()
    value_t = graphene.String()
    value_u = graphene.String()
    value_u = graphene.String()


class ageObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Int()
    value_fr = graphene.Int()
    value_tr = graphene.String()

    def resolve_value_tr(root, info):
        return custom_translate(info.context.user, root["value"])


class languageObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_code = graphene.String()


class heightObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Int()
    value_fr = graphene.Int()
    value_tr = graphene.String()

    def resolve_value_tr(root, info):
        return custom_translate(info.context.user, root["value"])


class ethnicityObj(DefaultObj):
    pass


class familyObj(DefaultObj):
    pass


class genderObj(DefaultObj):
    pass


class searchGenderObj(DefaultObj):
    pass


class politicsObj(DefaultObj):
    pass


class religiousObj(DefaultObj):
    pass


class tagsObj(DefaultObj):
    pass


class zodiacSignObj(DefaultObj):
    pass


class interestedInObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()
    value_tr = graphene.String()

    def resolve_value_tr(root, info):
        return custom_translate(info.context.user, root["value"])


class configObj(graphene.ObjectType):
    id = graphene.Int()
    message = graphene.String()
    imageMessage = graphene.String()
    avatarPhoto = graphene.Int()


class AllPickers(graphene.ObjectType):
    agePicker = graphene.List(ageObj)
    languagePicker = graphene.List(languageObj)
    ethnicityPicker = graphene.List(ethnicityObj)
    familyPicker = graphene.List(familyObj)
    genderPicker = graphene.List(genderObj)
    heightsPicker = graphene.List(heightObj)
    searchGendersPicker = graphene.List(searchGenderObj)
    politicsPicker = graphene.List(politicsObj)
    religiousPicker = graphene.List(religiousObj)
    tagsPicker = graphene.List(tagsObj)
    zodiacSignPicker = graphene.List(zodiacSignObj)
    configPicker = graphene.List(configObj)

    # interestedInPicker = graphene.List(interestedInObj)

    def resolve_agePicker(self, info):
        return age.objects.values("id", value=F("age"), value_fr=F("age"))

    def resolve_languagePicker(self, info):
        return Language.objects.values(
            "id", value=F("language"), value_code=F("language_code")
        )

    def resolve_heightsPicker(self, info):
        return height.objects.values("id", value=F("height"), value_fr=F("height"))

    def resolve_genderPicker(self, info):
        return gender.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "gender")),
            value_fr=F("gender_fr"),
            value_zh_cn=F("gender_zh_cn"),
            value_nl=F("gender_nl"),
            value_de=F("gender_de"),
            value_sw=F("gender_sw"),
            value_it=F("gender_it"),
            value_ar=F("gender_ar"),
            value_iw=F("gender_iw"),
            value_ja=F("gender_ja"),
            value_ru=F("gender_ru"),
            value_fa=F("gender_fa"),
            value_pt_br=F("gender_pt_br"),
            value_pt_pt=F("gender_pt_pt"),
            value_es=F("gender_es"),
            value_es_419=F("gender_es_419"),
            value_el=F("gender_el"),
            value_zh_tw=F("gender_zh_tw"),
            value_uk=F("gender_uk"),
            value_ko=F("gender_ko"),
            value_br=F("gender_br"),
            value_pl=F("gender_pl"),
            value_vi=F("gender_vi"),
            value_no=F("gender_no"),
            value_sv=F("gender_sv"),
            value_hr=F("gender_hr"),
            value_cs=F("gender_cs"),
            value_da=F("gender_da"),
            value_tl=F("gender_tl"),
            value_fi=F("gender_fi"),
            value_sl=F("gender_sl"),
            value_sq=F("gender_sq"),
            value_am=F("gender_am"),
            value_hy=F("gender_hy"),
            value_la=F("gender_la"),
            value_lv=F("gender_lv"),
            value_th=F("gender_th"),
            value_az=F("gender_az"),
            value_eu=F("gender_eu"),
            value_be=F("gender_be"),
            value_bn=F("gender_bn"),
            value_bs=F("gender_bs"),
            value_bg=F("gender_bg"),
            value_km=F("gender_km"),
            value_ca=F("gender_ca"),
            value_et=F("gender_et"),
            value_gl=F("gender_gl"),
            value_ka=F("gender_ka"),
            value_hi=F("gender_hi"),
            value_hu=F("gender_hu"),
            value_is=F("gender_is"),
            value_id=F("gender_id"),
            value_ga=F("gender_ga"),
            value_mk=F("gender_mk"),
            value_mn=F("gender_mn"),
            value_ne=F("gender_ne"),
            value_ro=F("gender_ro"),
            value_sr=F("gender_sr"),
            value_sk=F("gender_sk"),
            value_ta=F("gender_ta"),
            value_tg=F("gender_tg"),
            value_tr=F("gender_tr"),
            value_ur=F("gender_ur"),
            value_uz=F("gender_uz"),
        )

    def resolve_searchGendersPicker(self, info):
        return searchGender.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "searchGender")),
            value_fr=F("searchGender_fr"),
            value_zh_cn=F("searchGender_zh_cn"),
            value_nl=F("searchGender_nl"),
            value_de=F("searchGender_de"),
            value_sw=F("searchGender_sw"),
            value_it=F("searchGender_it"),
            value_ar=F("searchGender_ar"),
            value_iw=F("searchGender_iw"),
            value_ja=F("searchGender_ja"),
            value_ru=F("searchGender_ru"),
            value_fa=F("searchGender_fa"),
            value_pt_br=F("searchGender_pt_br"),
            value_pt_pt=F("searchGender_pt_pt"),
            value_es=F("searchGender_es"),
            value_es_419=F("searchGender_es_419"),
            value_el=F("searchGender_el"),
            value_zh_tw=F("searchGender_zh_tw"),
            value_uk=F("searchGender_uk"),
            value_ko=F("searchGender_ko"),
            value_br=F("searchGender_br"),
            value_pl=F("searchGender_pl"),
            value_vi=F("searchGender_vi"),
            value_no=F("searchGender_no"),
            value_sv=F("searchGender_sv"),
            value_hr=F("searchGender_hr"),
            value_cs=F("searchGender_cs"),
            value_da=F("searchGender_da"),
            value_tl=F("searchGender_tl"),
            value_fi=F("searchGender_fi"),
            value_sl=F("searchGender_sl"),
            value_sq=F("searchGender_sq"),
            value_am=F("searchGender_am"),
            value_hy=F("searchGender_hy"),
            value_la=F("searchGender_la"),
            value_lv=F("searchGender_lv"),
            value_th=F("searchGender_th"),
            value_az=F("searchGender_az"),
            value_eu=F("searchGender_eu"),
            value_be=F("searchGender_be"),
            value_bn=F("searchGender_bn"),
            value_bs=F("searchGender_bs"),
            value_bg=F("searchGender_bg"),
            value_km=F("searchGender_km"),
            value_ca=F("searchGender_ca"),
            value_et=F("searchGender_et"),
            value_gl=F("searchGender_gl"),
            value_ka=F("searchGender_ka"),
            value_hi=F("searchGender_hi"),
            value_hu=F("searchGender_hu"),
            value_is=F("searchGender_is"),
            value_id=F("searchGender_id"),
            value_ga=F("searchGender_ga"),
            value_mk=F("searchGender_mk"),
            value_mn=F("searchGender_mn"),
            value_ne=F("searchGender_ne"),
            value_ro=F("searchGender_ro"),
            value_sr=F("searchGender_sr"),
            value_sk=F("searchGender_sk"),
            value_ta=F("searchGender_ta"),
            value_tg=F("searchGender_tg"),
            value_tr=F("searchGender_tr"),
            value_ur=F("searchGender_ur"),
            value_uz=F("searchGender_uz"),
        )

    def resolve_ethnicityPicker(self, info):
        return ethnicity.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "ethnicity")),
            value_fr=F("ethnicity_fr"),
            value_zh_cn=F("ethnicity_zh_cn"),
            value_nl=F("ethnicity_nl"),
            value_de=F("ethnicity_de"),
            value_sw=F("ethnicity_sw"),
            value_it=F("ethnicity_it"),
            value_ar=F("ethnicity_ar"),
            value_iw=F("ethnicity_iw"),
            value_ja=F("ethnicity_ja"),
            value_ru=F("ethnicity_ru"),
            value_fa=F("ethnicity_fa"),
            value_pt_br=F("ethnicity_pt_br"),
            value_pt_pt=F("ethnicity_pt_pt"),
            value_es=F("ethnicity_es"),
            value_es_419=F("ethnicity_es_419"),
            value_el=F("ethnicity_el"),
            value_zh_tw=F("ethnicity_zh_tw"),
            value_uk=F("ethnicity_uk"),
            value_ko=F("ethnicity_ko"),
            value_br=F("ethnicity_br"),
            value_pl=F("ethnicity_pl"),
            value_vi=F("ethnicity_vi"),
            value_nn=F("ethnicity_nn"),
            value_no=F("ethnicity_no"),
            value_sv=F("ethnicity_sv"),
            value_hr=F("ethnicity_hr"),
            value_cs=F("ethnicity_cs"),
            value_da=F("ethnicity_da"),
            value_tl=F("ethnicity_tl"),
            value_fi=F("ethnicity_fi"),
            value_sl=F("ethnicity_sl"),
            value_sq=F("ethnicity_sq"),
            value_am=F("ethnicity_am"),
            value_hy=F("ethnicity_hy"),
            value_la=F("ethnicity_la"),
            value_lv=F("ethnicity_lv"),
            value_th=F("ethnicity_th"),
            value_az=F("ethnicity_az"),
            value_eu=F("ethnicity_eu"),
            value_be=F("ethnicity_be"),
            value_bn=F("ethnicity_bn"),
            value_bs=F("ethnicity_bs"),
            value_bg=F("ethnicity_bg"),
            value_km=F("ethnicity_km"),
            value_ca=F("ethnicity_ca"),
            value_et=F("ethnicity_et"),
            value_gl=F("ethnicity_gl"),
            value_ka=F("ethnicity_ka"),
            value_hi=F("ethnicity_hi"),
            value_hu=F("ethnicity_hu"),
            value_is=F("ethnicity_is"),
            value_id=F("ethnicity_id"),
            value_ga=F("ethnicity_ga"),
            value_mk=F("ethnicity_mk"),
            value_mn=F("ethnicity_mn"),
            value_ne=F("ethnicity_ne"),
            value_ro=F("ethnicity_ro"),
            value_sr=F("ethnicity_sr"),
            value_sk=F("ethnicity_sk"),
            value_ta=F("ethnicity_ta"),
            value_tg=F("ethnicity_tg"),
            value_tr=F("ethnicity_tr"),
            value_ur=F("ethnicity_ur"),
            value_uz=F("ethnicity_uz"),
        )

    def resolve_familyPicker(self, info):
        return family.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "familyPlans")),
            value_fr=F("familyPlans_fr"),
            value_zh_cn=F("familyPlans_zh_cn"),
            value_nl=F("familyPlans_nl"),
            value_de=F("familyPlans_de"),
            value_sw=F("familyPlans_sw"),
            value_it=F("familyPlans_it"),
            value_ar=F("familyPlans_ar"),
            value_iw=F("familyPlans_iw"),
            value_ja=F("familyPlans_ja"),
            value_ru=F("familyPlans_ru"),
            value_fa=F("familyPlans_fa"),
            value_pt_br=F("familyPlans_pt_br"),
            value_pt_pt=F("familyPlans_pt_pt"),
            value_es=F("familyPlans_es"),
            value_es_419=F("familyPlans_es_419"),
            value_el=F("familyPlans_el"),
            value_zh_tw=F("familyPlans_zh_tw"),
            value_uk=F("familyPlans_uk"),
            value_ko=F("familyPlans_ko"),
            value_br=F("familyPlans_br"),
            value_pl=F("familyPlans_pl"),
            value_vi=F("familyPlans_vi"),
            value_no=F("familyPlans_no"),
            value_sv=F("familyPlans_sv"),
            value_hr=F("familyPlans_hr"),
            value_cs=F("familyPlans_cs"),
            value_da=F("familyPlans_da"),
            value_tl=F("familyPlans_tl"),
            value_fi=F("familyPlans_fi"),
            value_sl=F("familyPlans_sl"),
            value_sq=F("familyPlans_sq"),
            value_am=F("familyPlans_am"),
            value_hy=F("familyPlans_hy"),
            value_la=F("familyPlans_la"),
            value_lv=F("familyPlans_lv"),
            value_th=F("familyPlans_th"),
            value_az=F("familyPlans_az"),
            value_eu=F("familyPlans_eu"),
            value_be=F("familyPlans_be"),
            value_bn=F("familyPlans_bn"),
            value_bs=F("familyPlans_bs"),
            value_bg=F("familyPlans_bg"),
            value_km=F("familyPlans_km"),
            value_ca=F("familyPlans_ca"),
            value_et=F("familyPlans_et"),
            value_gl=F("familyPlans_gl"),
            value_ka=F("familyPlans_ka"),
            value_hi=F("familyPlans_hi"),
            value_hu=F("familyPlans_hu"),
            value_is=F("familyPlans_is"),
            value_id=F("familyPlans_id"),
            value_ga=F("familyPlans_ga"),
            value_mk=F("familyPlans_mk"),
            value_mn=F("familyPlans_mn"),
            value_ne=F("familyPlans_ne"),
            value_ro=F("familyPlans_ro"),
            value_sr=F("familyPlans_sr"),
            value_sk=F("familyPlans_sk"),
            value_ta=F("familyPlans_ta"),
            value_tg=F("familyPlans_tg"),
            value_tr=F("familyPlans_tr"),
            value_ur=F("familyPlans_ur"),
            value_uz=F("familyPlans_uz"),
        )

    def resolve_politicsPicker(self, info):
        return politics.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "politics")),
            value_fr=F("politics_fr"),
            value_zh_cn=F("politics_zh_cn"),
            value_nl=F("politics_nl"),
            value_de=F("politics_de"),
            value_sw=F("politics_sw"),
            value_it=F("politics_it"),
            value_ar=F("politics_ar"),
            value_iw=F("politics_iw"),
            value_ja=F("politics_ja"),
            value_ru=F("politics_ru"),
            value_fa=F("politics_fa"),
            value_pt_br=F("politics_pt_br"),
            value_pt_pt=F("politics_pt_pt"),
            value_es=F("politics_es"),
            value_es_419=F("politics_es_419"),
            value_el=F("politics_el"),
            value_zh_tw=F("politics_zh_tw"),
            value_uk=F("politics_uk"),
            value_ko=F("politics_ko"),
            value_br=F("politics_br"),
            value_pl=F("politics_pl"),
            value_vi=F("politics_vi"),
            value_no=F("politics_no"),
            value_sv=F("politics_sv"),
            value_hr=F("politics_hr"),
            value_cs=F("politics_cs"),
            value_da=F("politics_da"),
            value_tl=F("politics_tl"),
            value_fi=F("politics_fi"),
            value_sl=F("politics_sl"),
            value_sq=F("politics_sq"),
            value_am=F("politics_am"),
            value_hy=F("politics_hy"),
            value_la=F("politics_la"),
            value_lv=F("politics_lv"),
            value_th=F("politics_th"),
            value_az=F("politics_az"),
            value_eu=F("politics_eu"),
            value_be=F("politics_be"),
            value_bn=F("politics_bn"),
            value_bs=F("politics_bs"),
            value_bg=F("politics_bg"),
            value_km=F("politics_km"),
            value_ca=F("politics_ca"),
            value_et=F("politics_et"),
            value_gl=F("politics_gl"),
            value_ka=F("politics_ka"),
            value_hi=F("politics_hi"),
            value_hu=F("politics_hu"),
            value_is=F("politics_is"),
            value_id=F("politics_id"),
            value_ga=F("politics_ga"),
            value_mk=F("politics_mk"),
            value_mn=F("politics_mn"),
            value_ne=F("politics_ne"),
            value_ro=F("politics_ro"),
            value_sr=F("politics_sr"),
            value_sk=F("politics_sk"),
            value_ta=F("politics_ta"),
            value_tg=F("politics_tg"),
            value_tr=F("politics_tr"),
            value_ur=F("politics_ur"),
            value_uz=F("politics_uz"),
        )

    def resolve_configPicker(self, info):
        return config.objects.values(
            "id",
            message=F("coinsPerMessage"),
            imageMessage=F("coinsPerPhotoMessage"),
            avatarPhoto=F("coinsPerAvatarPhoto"),
        )

    def resolve_religiousPicker(self, info):
        return religious.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "religious")),
            value_fr=F("religious_fr"),
            value_zh_cn=F("religious_zh_cn"),
            value_nl=F("religious_nl"),
            value_de=F("religious_de"),
            value_sw=F("religious_sw"),
            value_it=F("religious_it"),
            value_ar=F("religious_ar"),
            value_iw=F("religious_iw"),
            value_ja=F("religious_ja"),
            value_ru=F("religious_ru"),
            value_fa=F("religious_fa"),
            value_pt_br=F("religious_pt_br"),
            value_pt_pt=F("religious_pt_pt"),
            value_es=F("religious_es"),
            value_es_419=F("religious_es_419"),
            value_el=F("religious_el"),
            value_zh_tw=F("religious_zh_tw"),
            value_uk=F("religious_uk"),
            value_ko=F("religious_ko"),
            value_br=F("religious_br"),
            value_pl=F("religious_pl"),
            value_vi=F("religious_vi"),
            value_no=F("religious_no"),
            value_sv=F("religious_sv"),
            value_hr=F("religious_hr"),
            value_cs=F("religious_cs"),
            value_da=F("religious_da"),
            value_tl=F("religious_tl"),
            value_fi=F("religious_fi"),
            value_sl=F("religious_sl"),
            value_sq=F("religious_sq"),
            value_am=F("religious_am"),
            value_hy=F("religious_hy"),
            value_la=F("religious_la"),
            value_lv=F("religious_lv"),
            value_th=F("religious_th"),
            value_az=F("religious_az"),
            value_eu=F("religious_eu"),
            value_be=F("religious_be"),
            value_bn=F("religious_bn"),
            value_bs=F("religious_bs"),
            value_bg=F("religious_bg"),
            value_km=F("religious_km"),
            value_ca=F("religious_ca"),
            value_et=F("religious_et"),
            value_gl=F("religious_gl"),
            value_ka=F("religious_ka"),
            value_hi=F("religious_hi"),
            value_hu=F("religious_hu"),
            value_is=F("religious_is"),
            value_id=F("religious_id"),
            value_ga=F("religious_ga"),
            value_mk=F("religious_mk"),
            value_mn=F("religious_mn"),
            value_ne=F("religious_ne"),
            value_ro=F("religious_ro"),
            value_sr=F("religious_sr"),
            value_sk=F("religious_sk"),
            value_ta=F("religious_ta"),
            value_tg=F("religious_tg"),
            value_tr=F("religious_tr"),
            value_ur=F("religious_ur"),
            value_uz=F("religious_uz"),
        )

    def resolve_tagsPicker(self, info):
        return tags.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "tag")),
            value_fr=F("tag_fr"),
            value_zh_cn=F("tag_zh_cn"),
            value_nl=F("tag_nl"),
            value_de=F("tag_de"),
            value_sw=F("tag_sw"),
            value_it=F("tag_it"),
            value_ar=F("tag_ar"),
            value_iw=F("tag_iw"),
            value_ja=F("tag_ja"),
            value_ru=F("tag_ru"),
            value_fa=F("tag_fa"),
            value_pt_br=F("tag_pt_br"),
            value_pt_pt=F("tag_pt_pt"),
            value_es=F("tag_es"),
            value_es_419=F("tag_es_419"),
            value_el=F("tag_el"),
            value_zh_tw=F("tag_zh_tw"),
            value_uk=F("tag_uk"),
            value_ko=F("tag_ko"),
            value_br=F("tag_br"),
            value_pl=F("tag_pl"),
            value_vi=F("tag_vi"),
            value_nn=F("tag_nn"),
            value_no=F("tag_no"),
            value_sv=F("tag_sv"),
            value_hr=F("tag_hr"),
            value_cs=F("tag_cs"),
            value_da=F("tag_da"),
            value_tl=F("tag_tl"),
            value_fi=F("tag_fi"),
            value_sl=F("tag_sl"),
            value_sq=F("tag_sq"),
            value_am=F("tag_am"),
            value_hy=F("tag_hy"),
            value_la=F("tag_la"),
            value_lv=F("tag_lv"),
            value_th=F("tag_th"),
            value_az=F("tag_az"),
            value_eu=F("tag_eu"),
            value_be=F("tag_be"),
            value_bn=F("tag_bn"),
            value_bs=F("tag_bs"),
            value_bg=F("tag_bg"),
            value_km=F("tag_km"),
            value_ca=F("tag_ca"),
            value_et=F("tag_et"),
            value_gl=F("tag_gl"),
            value_ka=F("tag_ka"),
            value_hi=F("tag_hi"),
            value_hu=F("tag_hu"),
            value_is=F("tag_is"),
            value_id=F("tag_id"),
            value_ga=F("tag_ga"),
            value_mk=F("tag_mk"),
            value_mn=F("tag_mn"),
            value_ne=F("tag_ne"),
            value_ro=F("tag_ro"),
            value_sr=F("tag_sr"),
            value_sk=F("tag_sk"),
            value_ta=F("tag_ta"),
            value_tg=F("tag_tg"),
            value_tr=F("tag_tr"),
            value_ur=F("tag_ur"),
            value_uz=F("tag_uz"),
        )

    def resolve_zodiacSignPicker(self, info):
        return zodiacSign.objects.values(
            "id",
            value=F(translated_field_name(info.context.user, "zodiacSign")),
            value_fr=F("zodiacSign_fr"),
            value_zh_cn=F("zodiacSign_zh_cn"),
            value_nl=F("zodiacSign_nl"),
            value_de=F("zodiacSign_de"),
            value_sw=F("zodiacSign_sw"),
            value_it=F("zodiacSign_it"),
            value_ar=F("zodiacSign_ar"),
            value_iw=F("zodiacSign_iw"),
            value_ja=F("zodiacSign_ja"),
            value_ru=F("zodiacSign_ru"),
            value_fa=F("zodiacSign_fa"),
            value_pt_br=F("zodiacSign_pt_br"),
            value_pt_pt=F("zodiacSign_pt_pt"),
            value_es=F("zodiacSign_es"),
            value_es_419=F("zodiacSign_es_419"),
            value_el=F("zodiacSign_el"),
            value_zh_tw=F("zodiacSign_zh_tw"),
            value_uk=F("zodiacSign_uk"),
            value_ko=F("zodiacSign_ko"),
            value_br=F("zodiacSign_br"),
            value_pl=F("zodiacSign_pl"),
            value_vi=F("zodiacSign_vi"),
            value_nn=F("zodiacSign_nn"),
            value_no=F("zodiacSign_no"),
            value_sv=F("zodiacSign_sv"),
            value_hr=F("zodiacSign_hr"),
            value_cs=F("zodiacSign_cs"),
            value_da=F("zodiacSign_da"),
            value_tl=F("zodiacSign_tl"),
            value_fi=F("zodiacSign_fi"),
            value_sl=F("zodiacSign_sl"),
            value_sq=F("zodiacSign_sq"),
            value_am=F("zodiacSign_am"),
            value_hy=F("zodiacSign_hy"),
            value_la=F("zodiacSign_la"),
            value_lv=F("zodiacSign_lv"),
            value_th=F("zodiacSign_th"),
            value_az=F("zodiacSign_az"),
            value_eu=F("zodiacSign_eu"),
            value_be=F("zodiacSign_be"),
            value_bn=F("zodiacSign_bn"),
            value_bs=F("zodiacSign_bs"),
            value_bg=F("zodiacSign_bg"),
            value_km=F("zodiacSign_km"),
            value_ca=F("zodiacSign_ca"),
            value_et=F("zodiacSign_et"),
            value_gl=F("zodiacSign_gl"),
            value_ka=F("zodiacSign_ka"),
            value_hi=F("zodiacSign_hi"),
            value_hu=F("zodiacSign_hu"),
            value_is=F("zodiacSign_is"),
            value_id=F("zodiacSign_id"),
            value_ga=F("zodiacSign_ga"),
            value_mk=F("zodiacSign_mk"),
            value_mn=F("zodiacSign_mn"),
            value_ne=F("zodiacSign_ne"),
            value_ro=F("zodiacSign_ro"),
            value_sr=F("zodiacSign_sr"),
            value_sk=F("zodiacSign_sk"),
            value_ta=F("zodiacSign_ta"),
            value_tg=F("zodiacSign_tg"),
            value_tr=F("zodiacSign_tr"),
            value_ur=F("zodiacSign_ur"),
            value_uz=F("zodiacSign_uz"),
        )

    def resolve_interestedInPicker(self, info):
        return interestedIn.objects.values(
            "id", value=F("interest"), value_fr=F("interest_fr")
        )


class Query(graphene.ObjectType):
    defaultPicker = graphene.Field(AllPickers)

    def resolve_defaultPicker(self, info):
        return AllPickers()
