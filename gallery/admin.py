from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from easy_select2 import select2_modelform
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from .models import Album, Photo


class AlbumAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["image_tag"]
    search_fields = ["user__id", "user__username"]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
