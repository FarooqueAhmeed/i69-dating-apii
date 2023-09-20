from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .models import (
    age,
    height,
    gender,
    Language,
    searchGender,
    ethnicity,
    family,
    politics,
    religious,
    tags,
    zodiacSign,
    interestedIn,
    config,
    music,
    tvShows,
    sportsTeams,
    movies,
    book,
)


@admin.register(age)
class AgeAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ["id", "language", "language_code"]
    search_fields = ["language", "language_code"]
    ordering = ["id"]


@admin.register(height)
class HeightAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(config)
class ConfigAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(gender)
class GenderAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(searchGender)
class searchGenderAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(tags)
class TagAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ["id", "tag", "tag_fr"]
    search_fields = ["id", "tag", "tag_fr"]

    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(TagAdmin, self).changelist_view(request, extra_context)


@admin.register(ethnicity)
class EthnicityAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(politics)
class PoliticsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(religious)
class ReligiousAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(music)
class MusicAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(tvShows)
class TVShowAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(book)
class BookAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(BookAdmin, self).changelist_view(request, extra_context)


@admin.register(movies)
class MoviesAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(sportsTeams)
class SportTeamsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(zodiacSign)
class zodiacSignAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(family)
class FamilyAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(interestedIn)
class InterestedInAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ["id", "interest", "interest_fr"]
