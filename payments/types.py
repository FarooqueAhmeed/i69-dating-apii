import graphene
from graphene_django import DjangoObjectType
from .models import BokuPayment, SetAllowedPaymentMethods


class BokuPaymentType(DjangoObjectType):
    class Meta:
        model = BokuPayment
        fields = (
            "id",
            "charging_token",
            "authorisation_state",
            "billing_identity",
            "operation_reference",
        )


class StripePublishableKeyType(graphene.ObjectType):
    publishable_key = graphene.String(description="Stripe public key")


class PayPalPublishableKeyType(graphene.ObjectType):
    publishable_key = graphene.String(description="PayPal public key")


class SetAllowedPaymentMethodsType(DjangoObjectType):
    class Meta:
        model = SetAllowedPaymentMethods
        fields = ["payment_method", "is_allowed"]


class PaymentGatewayForRegionType(graphene.ObjectType):
    payment_method = graphene.String()
    is_allowed = graphene.Boolean()
