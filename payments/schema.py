import graphene
import stripe
import channels_graphql_ws
from django.shortcuts import get_object_or_404
from geopy.geocoders import Nominatim
import json
import traceback

from payments.boku import Boku
from user.models import User

from .models import (
    BokuPayment,
    Charge,
    Operator,
    PrivateKey,
    PublicKey,
    StripeIntent,
    PayPalOrder,
    SetAllowedPaymentMethods,
    PaymentGatewayForRegion,
    SetPaymentMethodRegion
)
from .paypal import PayPal
from .google import Google
from django.db.models import Q
from .types import (
    PayPalPublishableKeyType,
    StripePublishableKeyType,
    BokuPaymentType,
    SetAllowedPaymentMethodsType,
    PaymentGatewayForRegionType
)

from user.utils import translate_error_message


class AvailableBokuOperatorsResponse(graphene.ObjectType):
    operators = graphene.List(graphene.String)


class MobilePinInputResponse(graphene.ObjectType):
    operation_reference = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class ChargePaymentResponse(graphene.ObjectType):
    charging_token = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class RefundPaymentResponse(graphene.ObjectType):
    payment_reference = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class PinAuthorisationResponse(graphene.ObjectType):
    operation_reference = graphene.String()
    id = graphene.Int()
    user_id = graphene.Int()
    success = graphene.Boolean()


class AvailableBokuOperators(graphene.Mutation):
    class Arguments:
        latitude = graphene.String()
        longitude = graphene.String()

    Output = AvailableBokuOperatorsResponse

    def mutate(self, info, latitude, longitude):
        geolocator = Nominatim(user_agent="framework")
        location = geolocator.reverse(
            "%s, %s" % (latitude, longitude), exactly_one=True
        )
        country = location.address.split(",")[-1].strip()

        operators_list = list(
            Operator.objects.filter(
                country=country).values_list("code", flat=True)
        )

        return AvailableBokuOperatorsResponse(operators=operators_list)


class MobilePinInputMutation(graphene.Mutation):
    class Arguments:
        code = graphene.Int()
        charging_token = graphene.String()

    Output = MobilePinInputResponse

    def mutate(self, info, code, charging_token):
        boku_payment = get_object_or_404(
            BokuPayment, charging_token=charging_token)
        boku = Boku()
        callback = (
            info.context.headers["Origin"] +
            "/payments/webhook/boku/authorisation/"
        )
        # callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/authorisation/"
        body = {
            "flow": {
                "pin": {
                    "channel_code": "sandbox-ee",
                    "msisdn": boku_payment.billing_identity,
                    "code": str(code),
                }
            },
            "country": "EE",
            "merchant": os.getenv("MERCHANT_ID", None),
            "operation_reference": boku_payment.operation_reference,
            "callback": callback,
        }

        url = "https://api-jwt.fortumo.io/authorisations/" + \
            str(charging_token)

        response = boku.make_put_request(url, body=body)

        if response:
            return MobilePinInputResponse(
                operation_reference=boku_payment.operation_reference,
                id=id,
                success=True,
            )
        else:
            return MobilePinInputResponse(operation_reference="", id=0, success=False)


class RefundPaymentMutation(graphene.Mutation):
    class Arguments:
        payment_reference = graphene.String()
        refund_reason = graphene.String()
        amount = graphene.Float()

    Output = RefundPaymentResponse

    def mutate(self, info, payment_reference, amount, refund_reason):
        charge = get_object_or_404(
            Charge, operation_reference=payment_reference)

        boku = Boku()

        callback = info.context.headers["Origin"] + \
            "/payments/webhook/boku/refund/"
        # callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/refund/"

        body = {
            "payment_operation_reference": payment_reference,
            "refund_reason": refund_reason,
            "merchant": os.getenv("MERCHANT_REFUND_ID", None),
            "operation_reference": "refund_" + str(charge.payment.id),
            "callback": callback,
            "amount": {"value": amount, "currency": "EUR"},
        }

        url = "https://api-jwt.fortumo.io/refunds"

        response = boku.make_post_request(url, body=body)

        if response:
            return RefundPaymentResponse(
                payment_reference=payment_reference, success=True
            )
        else:
            return RefundPaymentResponse(
                payment_reference=payment_reference, success=False
            )


class ChargePaymentMutation(graphene.Mutation):
    class Arguments:
        charging_token = graphene.String()
        amount = graphene.Float()
        description = graphene.String()

    Output = ChargePaymentResponse

    def mutate(self, info, charging_token, amount, description):
        boku_payment = get_object_or_404(
            BokuPayment, charging_token=charging_token)

        boku = Boku()

        callback = info.context.headers["Origin"] + \
            "/payments/webhook/boku/charge/"
        # callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/charge/"

        body = {
            "item_description": description,
            "amount": {"value": str(amount), "currency": "EUR"},
            "charging_token": charging_token,
            "merchant": os.getenv("MERCHANT_ID", None),
            "operation_reference": "charge-payment" + str(boku_payment.id),
            "callback": callback,
        }

        url = "https://api-jwt.fortumo.io/payments"

        response = boku.make_post_request(url, body=body)

        if response:
            return ChargePaymentResponse(
                charging_token=boku_payment.charging_token, success=True
            )
        else:
            return MobilePinInputResponse(
                charging_token=boku_payment.charging_token, success=False
            )


class PinAuthorisationMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.String()
        mobile_number = graphene.String()
        recurring_payment = graphene.Boolean()
        operator_code = graphene.String()

    Output = PinAuthorisationResponse

    def mutate(self, info, mobile_number, recurring_payment, user_id, operator_code):
        user = User.objects.get(id=user_id)
        boku_payment = BokuPayment(operation_reference="initial")
        boku = Boku()

        boku_payment.save()

        id = boku_payment.id

        operation_reference = "payment" + str(id)

        boku_payment.operation_reference = operation_reference
        boku_payment.user = user
        payment_type = "onetime"

        if recurring_payment:
            payment_type = "subscription"

        callback = (
            info.context.headers["Origin"] +
            "/payments/webhook/boku/authorisation/"
        )
        # callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/authorisation/"
        body = {
            "flow": {
                "pin": {
                    "channel_code": operator_code,
                    "msisdn": mobile_number,
                    "code": "",
                }
            },
            "country": "EE",
            "merchant": os.getenv("MERCHANT_ID", None),
            "operation_reference": operation_reference,
            "callback": callback,
            "payment_type": payment_type,
        }

        boku_payment.billing_identity = mobile_number

        response = boku.make_post_request(
            "https://api-jwt.fortumo.io/authorisations", body=body
        )

        if response:
            boku_payment.save()
            return PinAuthorisationResponse(
                operation_reference=operation_reference, id=id, success=True
            )
        else:
            boku_payment.delete()
            return PinAuthorisationResponse(operation_reference="", id=0, success=False)


class StripeCreateIntentMutation(graphene.Mutation):
    class Arguments:
        amount = graphene.Float()
        currency = graphene.String()
        payment_method_type = graphene.String()

    client_secret = graphene.String()

    def mutate(self, info, amount, currency="usd", payment_method_type="card"):
        private_key = PrivateKey.objects.filter(
            payment_gateway="stripe").first()
        if not private_key:
            raise Exception(translate_error_message(
                info.context.user, "Stripe is not configured. Please try again latter."))

        stripe.api_key = private_key.key_text

        params = {
            "payment_method_types": [payment_method_type],
            "amount": int(amount * 100),
            "currency": currency,
            "metadata": {
                "user_id": info.context.user.id,
                "user_name": info.context.user.username,
                "purpose": "PURCHASE COINS",
            },
        }

        if payment_method_type == "acss_debit":
            params["payment_method_options"] = {
                "acss_debit": {
                    "mandate_options": {
                        "payment_schedule": "sporadic",
                        "transaction_type": "personal",
                    }
                }
            }
        try:
            intent = stripe.PaymentIntent.create(**params)
            intent_instance = StripeIntent.objects.create(
                user=info.context.user,
                status=intent.status,
                amount=intent.amount / 100,
                currency=intent.currency,
                intent_id=intent.id,
            )
            return StripeCreateIntentMutation(client_secret=intent.client_secret)
        except stripe.error.StripeError as e:
            raise Exception(translate_error_message(
                info.context.user, f"Failed to create stripe intent. error: {str(e)}"))
        except Exception as e:
            raise Exception(translate_error_message(
                info.context.user, f"Failed to create stripe intent.{str(e)}"))


class StripePaymentSuccessMutation(graphene.Mutation):
    class Arguments:
        intent_id = graphene.String(required=True)
        status = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, intent_id, status):
        intent = StripeIntent.objects.filter(intent_id=intent_id).first()
        if not intent:
            raise Exception(translate_error_message(
                info.context.user, "Invalid intent id."))

        private_key = PrivateKey.objects.filter(
            payment_gateway="stripe").first()
        if not private_key:
            raise Exception(translate_error_message(
                info.context.user, "Stripe is not configured. Please try again latter."))

        try:
            stripe.api_key = private_key.key_text

            intent = stripe.PaymentIntent.retrieve(id=intent_id)

            if intent.status != status:
                raise Exception(translate_error_message(
                    info.context.user, "Invalid status"))

            update_data = {"status": intent["status"]}
            if intent.status == "succeeded":
                update_data["charge_id"] = intent["charges"]["data"][0]["id"]
                update_data["payment_method_id"] = intent["charges"]["data"][0][
                    "payment_method"
                ]
            StripeIntent.objects.filter(
                intent_id=intent_id).update(**update_data)
            return StripePaymentSuccessMutation(
                success=True, message=translate_error_message(info.context.user, "Payment completed successfully")
            )

        except Exception as e:
            print(e)
            raise Exception(translate_error_message(
                info.context.user, "Invalid payment intent"))


class StripePaymentRefundMutation(graphene.Mutation):
    class Arguments:
        intent_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, intent_id):
        intent = StripeIntent.objects.filter(intent_id=intent_id).first()
        if not intent:
            raise Exception(translate_error_message(
                info.context.user, "Invalid intent id."))

        private_key = PrivateKey.objects.filter(
            payment_gateway="stripe").first()
        if not private_key:
            raise Exception(translate_error_message(
                info.context.user, "Stripe is not configured. Please try again latter."))

        stripe.api_key = private_key.key_text

        refund = stripe.Refund.create(payment_intent=intent_id)

        print(refund)
        return StripePaymentRefundMutation(
            success=True, message=translate_error_message(info.context.user, "Payment Refunded successfully")
        )


class PayPalCreateOrderMutation(graphene.Mutation):
    class Arguments:
        amount = graphene.Float(required=True)
        currency = graphene.String()

    id = graphene.String()
    status = graphene.String()

    def mutate(self, info, amount, currency="USD"):
        try:
            order = PayPal.create_order(amount=amount)
            PayPalOrder.objects.create(
                user=info.context.user,
                order_id=order["id"],
                status=order["status"],
                amount=amount,
                currency=currency,
            )
            return PayPalCreateOrderMutation(id=order["id"], status=order["status"])
        except Exception as e:
            print(e)
            raise Exception(translate_error_message(
                info.context.user, "Failed to create the order."))


class PayPalCapturePaymentMutation(graphene.Mutation):
    class Arguments:
        order_id = graphene.String(required=True)

    id = graphene.String()
    status = graphene.String()

    def mutate(self, info, order_id):
        try:
            payment_status = None
            payment_id = None
            payer_id = None
            payer_email_address = None
            payment = PayPal.capture_order_payment(order_id=order_id)
            print(json.dumps(payment.json(), indent=4, default=str))
            if payment.status_code == 400:
                payment_status = payment.json()['details'][0]['issue']
                payment_id = order_id
            else:
                payment_id = payment.json()["id"]
                payment_status = payment.json()["status"]
                payer_id = payment.json()["payer"]["payer_id"]
                payer_email_address = payment.json()["payer"]["email_address"]
            PayPalOrder.objects.filter(order_id=order_id).update(
                status=payment_status,
                customer_id=payer_id,
                customer_email=payer_email_address,
            )
            return PayPalCapturePaymentMutation(
                id=payment_id, status=payment_status
            )
        except Exception as e:
            print(e, traceback.print_exc())
            raise Exception(translate_error_message(
                info.context.user, "Failed to cpature payment."))


class PayPalCancelOrderMutation(graphene.Mutation):
    class Arguments:
        order_id = graphene.String()

    id = graphene.String()
    status = graphene.String()

    def mutate(self, info, order_id):
        try:
            PayPalOrder.objects.filter(
                order_id=order_id).update(status="CANCELLED")
            return PayPalCancelOrderMutation(id=order_id, status="CANCELLED")
        except Exception:
            raise Exception(translate_error_message(
                info.context.user, "Failed to update the order status"))


class GoogleCreateOrderMutation(graphene.Mutation):
    class Arguments:
        amount = graphene.Float(required=True)
        currency = graphene.String()
        order_id = graphene.String(required=True)
        status = graphene.String(required=True)

    status = graphene.String()
    statusCode = graphene.Int()

    def mutate(self, info, amount, currency="USD", order_id=None, status=None):
        try:
            order = Google.create_order(
                amount=amount, currency=currency, user=info.context.user, order_id=order_id, status=status)
            return GoogleCreateOrderMutation(statusCode=200, status="order created successfully")
        except Exception as e:
            print(e)
            raise Exception(translate_error_message(
                info.context.user, "Failed to create the order."))


class onPaymentMethodChange(channels_graphql_ws.Subscription):

    payment_method = graphene.String()
    is_allowed = graphene.Boolean()

    class Arguments:
        payment_method = graphene.String()
        is_allowed = graphene.String()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        payment_method = self["payment_method"]
        is_allowed = self["is_allowed"]
        return onPaymentMethodChange(
            payment_method=payment_method, is_allowed=is_allowed
        )


class Query(graphene.ObjectType):
    payment_by_operation_reference = graphene.Field(
        BokuPaymentType, operation_reference=graphene.String(required=True)
    )

    stripe_publishable_key = graphene.Field(StripePublishableKeyType)

    paypal_publishable_key = graphene.Field(PayPalPublishableKeyType)

    get_payment_methods = graphene.List(PaymentGatewayForRegionType)

    def resolve_get_payment_methods(self, info):
        user_obj = info.context.user
        payment_gateways = PaymentGatewayForRegion.objects.filter(
            Q(region__countries__name__iexact=user_obj.country_code), Q(
                is_allowed=True)
        ).values('payment_gateway__payment_method')
        allowed_payment_methods = SetAllowedPaymentMethods.objects.values(
            "payment_method")

        pay_objs = [
            {
                "payment_method": pay_obj["payment_method"],
                "is_allowed": any(
                    pay_obj["payment_method"] == gateway["payment_gateway__payment_method"]
                    for gateway in payment_gateways
                ),
            }
            for pay_obj in allowed_payment_methods
        ]
        return pay_objs

    def resolve_payment_by_operation_reference(root, info, operation_reference):
        try:
            return BokuPayment.objects.get(operation_reference=operation_reference)
        except BokuPayment.DoesNotExist:
            return None

    def resolve_stripe_publishable_key(self, info):
        try:
            stripe_key = PublicKey.objects.filter(
                payment_gateway="stripe").first()
            return StripePublishableKeyType(publishable_key=stripe_key.key_text)
        except PublicKey.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "Stripe is not configured. Please try again latter."))

    def resolve_paypal_publishable_key(self, info):
        try:
            key = PayPal.get_client_id()
            if not key:
                raise Exception(translate_error_message(
                    info.context.user, "PayPal is not configured!"))
            return PayPalPublishableKeyType(publishable_key=key)
        except Exception:
            return None


class Mutation(graphene.ObjectType):
    pin_authorisation = PinAuthorisationMutation.Field()
    mobile_pin_input = MobilePinInputMutation.Field()
    charge_payment = ChargePaymentMutation.Field()
    refund_payment = RefundPaymentMutation.Field()
    available_boku_operators = AvailableBokuOperators.Field()
    stripe_create_intent = StripeCreateIntentMutation.Field()
    stripe_payment_success = StripePaymentSuccessMutation.Field()
    stripe_payment_refund = StripePaymentRefundMutation.Field()
    paypal_create_order = PayPalCreateOrderMutation.Field()
    paypal_capture_payment = PayPalCapturePaymentMutation.Field()
    paypal_cancel_order = PayPalCancelOrderMutation.Field()
    google_create_order = GoogleCreateOrderMutation.Field()


class Subscription(graphene.ObjectType):
    on_payment_method_change = onPaymentMethodChange.Field()
