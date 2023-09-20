from django.contrib import admin
from django.contrib.admin.options import ModelAdmin, TabularInline
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.forms import BooleanField, ModelChoiceField, ModelMultipleChoiceField
from django.utils import timezone
from django.utils.html import format_html
from easy_select2 import Select2

from .filters import CancelPurchaseFilter, PackagePerHourFilter, PurchaseMethodFilter
from .forms import PackagePurchaseForm
from .models import (
    Package,
    PackagePermissionLimit,
    PackagePurchase,
    Permission,
    Plan,
    Purchase,
    CoinPrices,
    CoinPricesForRegion,
    PlanForRegion
)
from .utils import package_plans_duration_timedeltas

import nested_admin

class PurchaseAdmin(ModelAdmin):
    list_display = [
        "user",
        "purchased_on",
        "coins",
        "method",
        "money",
        "payment_method",
        "currency",
    ]
    search_fields = ["user__username", "user__fullName", "user__email"]
    date_hierarchy = "purchased_on"
    list_filter = ["user__country", PurchaseMethodFilter, PackagePerHourFilter]

    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(PurchaseAdmin, self).changelist_view(request, extra_context)


class PlanForRegionInline(nested_admin.NestedTabularInline):
    model = PlanForRegion
    extra = 0
    fields = ["region", "price_in_coins", "is_active"]


class PlanAdmin(nested_admin.NestedModelAdmin):
    list_display = ["title", "package", "price_in_coins", "validity"]
    inlines = [
        PlanForRegionInline
    ]


class PlanInline(nested_admin.NestedTabularInline):
    model = Plan
    fields = ["validity", "title", "price_in_coins", "is_active"]
    extra = 0
    prepopulated_fields = {"title": ("validity",)}
    show_change_link = True
    inlines = [
        PlanForRegionInline
    ]


class PermissionLimitInline(TabularInline):
    model = PackagePermissionLimit
    fields = ["package", "per_day", "per_week", "per_month", "is_unlimited"]
    extra = 0
    min_num = 3


class PackageAdmin(nested_admin.NestedModelAdmin):
    inlines = (PlanInline,)
    list_display = ["name", "description", "package_plans", "services"]
    search_fields = ["name", "description"]
    sortable_by = ["name"]
    ordering = ("id",)

    def package_plans(self, obj):
        plans = Plan.objects.filter(package=obj).order_by("id").all()
        plans_str = "</br>".join(
            [f"{plan.title} -> {plan.price_in_coins} COINS" for plan in plans]
        )
        return format_html(plans_str)

    def services(self, obj):
        return format_html("</br>".join([perm.name for perm in obj.permissions.all()]))

    package_plans.allow_tags = True
    package_plans.short_description = "Plan Prices"

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        form = super().get_form(request, obj, **defaults)
        form.base_fields["permissions"] = ModelMultipleChoiceField(
            label="Services",
            queryset=Permission.objects.all(),
            widget=FilteredSelectMultiple("Name", is_stacked=False),
            required=True,
        )
        return form


class PackagePurchaseAdmin(ModelAdmin):
    list_display = [
        "user",
        "package",
        "plan",
        "starts_at",
        "ends_at",
        "is_active",
        "cancelled",
        "cancelled_at",
        "upgraded_at",
        "upgraded_to_package",
    ]
    list_filter = ["is_active", "starts_at", "user__country", CancelPurchaseFilter]
    date_hierarchy = "starts_at"

    form = PackagePurchaseForm

    add_form_template = "admin/purchase/packagepurchase/change_form.html"
    change_form_template = "admin/purchase/packagepurchase/change_form.html"

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        defaults.update(
            {
                "help_texts": {
                    "plan": 'To change password use <a href="../password">this form</a>'
                }
            }
        )
        form = super().get_form(request, obj, **defaults)
        if not obj:
            plan = ModelChoiceField(
                queryset=Plan.objects.distinct("title"),
                required=True,
                to_field_name="id",
            )
            form.base_fields["plan"] = plan
        else:
            plan = ModelChoiceField(
                queryset=Plan.objects.filter(package=obj.package).order_by("id"),
                required=True,
                to_field_name="id",
            )
            form.base_fields["plan"] = plan

        form.base_fields["is_active"].initial = True

        if not obj:
            form.base_fields["user"] = ModelChoiceField(
                queryset=get_user_model().objects.filter(is_active=True),
                widget=Select2(select2attrs={"width": "300px"}),
                required=True,
            )
        else:
            form.base_fields.pop("user", None)
            form.base_fields["cancelled_at"] = BooleanField(
                required=False,
                initial=True if obj.cancelled_at is not None else False,
                label="Cancel subscription",
            )
        return form

    def cancelled(self, obj):
        return True if obj.cancelled_at is not None else False

    cancelled.boolean = True

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            user = obj.user
            user.deductCoins(obj.package_price, "Package purchase (admin)")
            user.save()
            super().save_model(request, obj, form, change)
        else:
            user = obj.user
            now = timezone.now()
            subscription = PackagePurchase.objects.filter(
                user=user, is_active=True, starts_at__lte=now, ends_at__gte=now
            ).first()

            if subscription:
                if subscription.package.id < obj.package_id:

                    # Calculate the upgrade price
                    remaining = 100 - (
                        timezone.now().timestamp() - subscription.starts_at.timestamp()
                    ) / (
                        subscription.ends_at.timestamp()
                        - subscription.starts_at.timestamp()
                    )
                    remaining = round(remaining, 2)

                    plan = Plan.objects.filter(
                        package_id=obj.package_id, title=obj.plan.title
                    ).first()
                    starts_at = subscription.starts_at
                    ends_at = starts_at + package_plans_duration_timedeltas.get(
                        plan.validity
                    )

                    if ends_at < now:
                        return

                    coins_needed = int(remaining * plan.price_in_coins)
                    user.deductCoins(coins_needed, "Package upgrade (admin)")
                    user.save()
                elif subscription.plan.id < obj.plan_id:
                    plan = Plan.objects.filter(
                        package_id=obj.package_id, title=obj.plan.title
                    ).first()
                    starts_at = subscription.starts_at
                    ends_at = starts_at + package_plans_duration_timedeltas.get(
                        plan.validity
                    )

                    if ends_at < now:
                        return

                    coins_needed = int(plan.price_in_coins)
                    user.deductCoins(coins_needed, "Plan upgrade (admin)")
                    user.save()

            super().save_model(request, obj, form, change)


class PermissionAdmin(ModelAdmin):
    inlines = [PermissionLimitInline]
    list_display = ["name", "user_free_limit", "description"]


class PackagePermissionLimitAdmin(ModelAdmin):

    fields = (
        "permission",
        "package",
        "per_day",
        "per_week",
        "per_month",
        "is_unlimited",
    )
    list_display = [
        "permission",
        "package",
        "per_day",
        "per_week",
        "per_month",
        "is_unlimited",
    ]
    list_filter = (
        "package",
        "permission",
    )


class CoinPricesForRegionInline(TabularInline):
    model = CoinPricesForRegion
    extra = 0
    can_delete = False


class CoinPricesAdmin(ModelAdmin):
    list_display = [
        "coins_count",
        "original_price",
        "discounted_price",
        "currency",
        "is_active",
    ]
    ordering = ("coins_count",)
    inlines = [
        CoinPricesForRegionInline
    ]


admin.site.register(Plan, PlanAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackagePurchase, PackagePurchaseAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PackagePermissionLimit, PackagePermissionLimitAdmin)
admin.site.register(CoinPrices, CoinPricesAdmin)
