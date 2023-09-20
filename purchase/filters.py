from django.contrib.admin import SimpleListFilter

from user.admin import PerHourFilter

from .utils import cancel_subscription_choices, payment_method_choices


class PackagePerHourFilter(PerHourFilter):
    column = "purchased_on"


class PurchaseMethodFilter(SimpleListFilter):
    title = "Purchase Method"
    parameter_name = "purchase_method"
    payments = [p[0] for p in payment_method_choices]

    def lookups(self, request, model_admin):
        return payment_method_choices

    def queryset(self, request, queryset):
        value = self.value()
        if value in self.payments:
            # purchase_user_ids = Purchase.objects.filter(payment_method=value).values("user_id").annotate(purchase_id=Max("purchase_id"))
            # purchase_user_ids = list(set([str(uid["user_id"]) for uid in purchase_user_ids]))
            # return queryset.filter(id__in=purchase_user_ids)
            return queryset.filter(payment_method__iexact=value)

        return queryset


class CancelPurchaseFilter(SimpleListFilter):
    title = "Cancelled Subscription"
    parameter_name = "cancelled_at"

    def lookups(self, request, model_admin):
        return cancel_subscription_choices

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(cancelled_at__isnull=False)
        elif value == "No":
            return queryset.filter(cancelled_at__isnull=True)

        return queryset
