from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Register your models here.

from .models import *

from easy_select2 import select2_modelform

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Reported_Users)
class Reported_UsersAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    search_fields = ["reporter", "reportee", "reason"]


@admin.register(GoogleAuth)
class GoogleAuthAdmin(admin.ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(GoogleAuthAdmin, self).changelist_view(request, extra_context)

from user.models import User

@admin.register(SocialAuthDetail)
class SocialAuthDetailAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ["provider", "status", "updated_by"]
    search_fields = ["provider", "updated_by__username"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["updated_by"].queryset = User.objects.filter(roles__role__in=["ADMIN", "SUPER_ADMIN"])
        return form
