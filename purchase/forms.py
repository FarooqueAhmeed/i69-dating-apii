from django.forms import ModelForm, ValidationError
from django.utils import timezone

from .models import PackagePurchase, Plan
from .utils import package_plans_duration_timedeltas


class PackagePurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PackagePurchase
        exclude = [
            "starts_at",
            "ends_at",
            "cancelled_at",
            "downgraded_at",
            "upgraded_at",
            "renewed_subscription",
            "renewed_at",
            "package_price",
            "purchase_price",
            "upgraded_to_package",
            "downgraded_to_package",
            "created_by_admin",
        ]

    def clean(self):
        self.cleaned_data = super(PackagePurchaseForm, self).clean()
        try:
            plan = Plan.objects.filter(
                package=self.cleaned_data["package"],
                title=self.cleaned_data["plan"].title,
            ).first()
            if not plan and self.instance.pk:
                raise ValidationError("Please choose a plan.")
        except Exception as e:
            raise ValidationError("Please choose a plan.")

        self.cleaned_data["package_price"] = plan.price_in_coins
        self.instance.package_price = plan.price_in_coins
        self.cleaned_data["purchased_price"] = plan.price_in_coins
        self.instance.purchased_price = plan.price_in_coins
        self.cleaned_data["created_by_admin"] = True
        self.instance.created_by_admin = True

        if plan.is_on_discount:
            self.cleaned_data["purchased_price"] = plan.dicounted_price_in_coins
            self.instance.purchased_price = plan.dicounted_price_in_coins

        starts_at = timezone.now()
        if self.instance.pk:
            starts_at = self.instance.starts_at
        ends_at = starts_at + package_plans_duration_timedeltas.get(plan.validity, None)

        self.cleaned_data["starts_at"] = starts_at
        self.instance.starts_at = starts_at
        self.cleaned_data["plan"] = plan
        self.instance.plan = plan

        self.cleaned_data["ends_at"] = ends_at
        self.instance.ends_at = ends_at

        if "cancelled_at" in self.cleaned_data:
            if self.cleaned_data["cancelled_at"] is True:
                self.cleaned_data["cancelled_at"] = timezone.now()
                self.instance.cancelled_at = timezone.now()
                self.instance.is_active = False
                self.cleaned_data["is_active"] = False
            else:
                self.cleaned_data["cancelled_at"] = None
                self.instance.cancelled_at = None

        # print("CLEANED DATA: ", self.cleaned_data, self.instance.pk)

        return self.cleaned_data
