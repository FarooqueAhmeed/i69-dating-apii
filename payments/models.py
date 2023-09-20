from django.db import models

from user.models import User, Country


payment_gateway_choices = (
    ("boku", "Boku"), ("stripe", "Stripe"), ("paypal", "PayPal"))


class Operator(models.Model):
    """
    Model to store the operator details
    """

    name = models.CharField(max_length=95)
    code = models.CharField(max_length=95)
    country = models.CharField(max_length=65)
    country_id = models.CharField(max_length=5)
    max_transaction_limit = models.FloatField()
    currency = models.CharField(max_length=65, default="euro")

    def __str__(self):
        return self.name + " " + self.country


class Msdin(models.Model):
    """
    Model to store the supported msdin for the country
    """

    operator = models.ForeignKey(
        Operator, on_delete=models.CASCADE, related_name="msdins"
    )
    pattern = models.CharField(max_length=55)


class PrivateKey(models.Model):
    """
    Model for parent API Keys
    """

    payment_gateway = models.CharField(
        max_length=65, choices=payment_gateway_choices)
    key_text = models.TextField()
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.payment_gateway + "(Private)"


class PublicKey(models.Model):
    """
    Model for public api keys
    """

    payment_gateway = models.CharField(
        max_length=65, choices=payment_gateway_choices)
    key_text = models.TextField()
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.payment_gateway + "(Public)"


class BokuPayment(models.Model):
    """
    Model to store the status of payments made via BOKU.
    """

    charging_token = models.CharField(max_length=65, blank=True)
    authorisation_state = models.CharField(max_length=20, blank=True)
    operation_reference = models.CharField(unique=True, max_length=65)
    consumer_identity = models.CharField(max_length=65, blank=True)
    latest_update = models.DateTimeField(blank=True, null=True)
    billing_identity = models.CharField(max_length=25, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.operation_reference


class BokuPaymentError(models.Model):
    """
    Model to store the errors if faces in a payment
    """

    payment = models.ForeignKey(
        BokuPayment, on_delete=models.CASCADE, related_name="errors"
    )
    message = models.CharField(max_length=155)


class Charge(models.Model):
    """
    Model to store the payments charged
    """

    payment = models.ForeignKey(
        BokuPayment, on_delete=models.SET_NULL, null=True, related_name="charges"
    )
    operation_reference = models.CharField(max_length=155)
    transaction_id = models.CharField(max_length=155)
    transaction_state = models.CharField(max_length=65)
    latest_update = models.DateTimeField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.transaction_id + " (%s)" % self.transaction_state


class ChargeError(models.Model):
    """
    Model to store the errors if faces in a payment
    """

    charge = models.ForeignKey(
        Charge, on_delete=models.CASCADE, related_name="errors")
    message = models.CharField(max_length=155)


class Refund(models.Model):
    """
    Model to store the refund processed
    """

    payment = models.ForeignKey(
        BokuPayment, on_delete=models.SET_NULL, null=True, related_name="refunds"
    )
    operation_reference = models.CharField(max_length=155)
    refund_reason = models.TextField(blank=True)
    refund_status = models.CharField(max_length=155, blank=True)
    amount = models.FloatField(blank=True, null=True)
    transaction_id = models.CharField(max_length=155)
    latest_update = models.DateTimeField(blank=True, null=True)


class RefundError(models.Model):
    """
    Model to store the errors if faces in a refund
    """

    refund = models.ForeignKey(
        Refund, on_delete=models.CASCADE, related_name="errors")
    message = models.CharField(max_length=155)


class StripeIntent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    status = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    intent_id = models.CharField(max_length=255, blank=True)
    payment_method_id = models.CharField(
        max_length=255, blank=True, null=True, default=None
    )
    charge_id = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    is_refunded = models.BooleanField(default=False, blank=True, null=True)
    refunded_at = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.intent_id} {self.status}"

    class Meta:
        verbose_name = "Stripe Order"
        verbose_name_plural = "Stripe Orders"


class StripeRefund(models.Model):
    intent = models.ForeignKey(
        StripeIntent, null=True, blank=True, on_delete=models.CASCADE
    )
    refund_reason = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )
    refund_status = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    udated_at = models.DateTimeField(auto_now=True)


class PayPalOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    order_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    customer_id = models.CharField(
        max_length=100, null=True, blank=True, default=None)
    customer_email = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.order_id}"

    class Meta:
        verbose_name = "PayPal Order"
        verbose_name_plural = "PayPal Orders"


class SetPaymentMethodRegion(models.Model):
    title = models.CharField(max_length=100, unique=True)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.title


class SetAllowedPaymentMethods(models.Model):
    """
    This method allows admin to choose the payment methods in the application
    """

    payment_method = models.CharField(max_length=100)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.payment_method} ---------> {self.is_allowed}"

    def save(self, *args, **kwargs):
        from payments import schema

        payment_method = self.payment_method
        is_allowed = self.is_allowed

        schema.onPaymentMethodChange.broadcast(
            group=None,
            payload={
                "payment_method": str(payment_method),
                "is_allowed": str(is_allowed),
            },
        )
        return super().save(*args, **kwargs)


class PaymentGatewayForRegion(models.Model):
    payment_gateway = models.ForeignKey(
        SetAllowedPaymentMethods, on_delete=models.CASCADE)
    region = models.ForeignKey(
        SetPaymentMethodRegion, on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=True)

    def __str__(self):
        return self.payment_gateway.payment_method + " (" + self.region.title + ")"

    class Meta:
        unique_together = ('payment_gateway', 'region')


class GoogleOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    order_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.order_id}"

    class Meta:
        verbose_name = "Google Order"
        verbose_name_plural = "Google Orders"
