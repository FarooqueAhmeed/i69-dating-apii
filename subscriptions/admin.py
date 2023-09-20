from django.contrib import admin

from subscriptions import models


# Register your models here.

@admin.register(models.SubscriptionsPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.ModeratorSubscriptionPlan)
class UserSubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["id", "moderator", "subscription"]
    autocomplete_fields = [
        "moderator",
    ]
