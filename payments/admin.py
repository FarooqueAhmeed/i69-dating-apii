from django.contrib import admin

from payments import models
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from user.forms import PaymentGatewayRegionForm


class PayPalOrderAdmin(admin.ModelAdmin):

    list_display = [
        "order_id",
        "user",
        "amount",
        "currency",
        "customer_id",
        "customer_email",
        "created_at",
        "updated_at",
        "completed",
    ]
    list_filter = ("status",)

    def completed(self, obj):
        return obj.status == "COMPLETED"

    def has_add_permission(self, request):
        return False

    completed.boolean = True


class StripeIntentAdmin(admin.ModelAdmin):
    list_display = [
        "intent_id",
        "user",
        "status",
        "amount",
        "currency",
        "created_at",
        "updated_at",
        "completed",
    ]
    list_filter = ("status",)

    def completed(self, obj):
        return obj.status == "succeeded"

    completed.boolean = True

    def has_add_permission(self, request):
        return False


class PaymentGatewayForRegionInline(admin.TabularInline):
    model = models.PaymentGatewayForRegion
    extra = 0
    can_delete = True


@admin.register(models.SetPaymentMethodRegion)
class SetPaymentMethodRegionAdmin(
    ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin
):
    search_fields = ["title"]
    filter_horizontal = ["countries"]
    form = PaymentGatewayRegionForm


class SetAllowedPaymentMethodsAdmin(admin.ModelAdmin):
    list_display = ["payment_method",]
    exclude = ('is_allowed',)
    list_filter = ("payment_method",)
    inlines = [PaymentGatewayForRegionInline]


class GoogleOrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "status", "amount", "currency", "created_at", "updated_at"]


admin.site.register(models.BokuPayment)
admin.site.register(models.BokuPaymentError)
admin.site.register(models.PrivateKey)
admin.site.register(models.PublicKey)
admin.site.register(models.Charge)
admin.site.register(models.ChargeError)
admin.site.register(models.Refund)
admin.site.register(models.RefundError)
admin.site.register(models.Operator)
admin.site.register(models.StripeIntent, StripeIntentAdmin)
admin.site.register(models.PayPalOrder, PayPalOrderAdmin)
admin.site.register(models.SetAllowedPaymentMethods, SetAllowedPaymentMethodsAdmin)
admin.site.register(models.GoogleOrder, GoogleOrderAdmin)
