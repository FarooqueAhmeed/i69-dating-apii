import datetime
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .models import (
    BokuPayment,
    BokuPaymentError,
    Charge,
    ChargeError,
    PayPalOrder,
    Refund,
    RefundError,
    StripeIntent,
)
from .paypal import PayPal


@csrf_exempt
def boku_refund_payment_callback(request):
    """
    Webhook to handle the callback from the boku's refund api
    """

    body = json.loads(request.body)

    refund, created = Refund.objects.get_or_create(
        operation_reference=body["operation_reference"]
    )

    boku_payment = BokuPayment.objects.get(
        consumer_identity=body["consumer_identity"], authorisation_state="verified"
    )

    timestamp = datetime.datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    refund.payment = boku_payment
    refund.refund_status = body["refund_status"]
    refund.amount = body["refund_amount"]["value"]
    refund.transaction_id = body["transaction_id"]
    refund.latest_update = timestamp

    refund.save()

    if body.get("error", None):
        error, created = RefundError.objects.get_or_create(refund=refund)

        error.message = body["error"]["message"]
        error.save()

    response = JsonResponse({"success": True})
    return response


@csrf_exempt
def boku_charge_payment_callback(request):
    """
    Webhook to handle the callback from the boku's charge api
    """
    body = json.loads(request.body)

    charge, created = Charge.objects.get_or_create(
        operation_reference=body["operation_reference"]
    )

    boku_payment = BokuPayment.objects.get(
        consumer_identity=body["consumer_identity"], authorisation_state="verified"
    )

    timestamp = datetime.datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    charge.payment = boku_payment

    charge.transaction_id = body["transaction_id"]
    charge.transaction_state = body["transaction_state"]
    charge.price = body["price"]["amount"]
    charge.latest_update = timestamp

    charge.save()

    if body.get("error", None):
        error, created = ChargeError.objects.get_or_create(charge=charge)

        error.message = body["error"]["message"]
        error.save()

    response = JsonResponse({"success": True})
    return response


@csrf_exempt
def boku_pin_authorisation_callback(request):
    """
    Webhook to handle the callback from the boku's pin authorization
    """

    body = json.loads(request.body)

    boku_payment = get_object_or_404(
        BokuPayment, operation_reference=body["operation_reference"]
    )

    timestamp = datetime.datetime.strptime(body["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

    boku_payment.charging_token = body["charging_token"]
    boku_payment.authorisation_state = body["authorisation_state"]
    boku_payment.latest_update = timestamp
    boku_payment.consumer_identity = body["consumer_identity"]

    boku_payment.save()

    if body.get("error", None):
        error, created = BokuPaymentError.objects.get_or_create(payment=boku_payment)

        error.message = body["error"]["message"]
        error.save()

    response = JsonResponse({"success": True})
    return response


@csrf_exempt
def stripe_webhook_callback(request):
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.body)
    # if webhook_secret:
    #     signature = request.headers.get('stripe-signature')
    #     try:
    #         event = stripe.Webhook.construct_event(
    #             payload=request.data, sig_header=signature, secret=webhook_secret)
    #         data = event['data']
    #     except Exception as e:
    #         return e
    #     event_type = event['type']
    # else:
    data = request_data["data"]
    event_type = request_data["type"]
    data_object = data["object"]

    if event_type == "payment_intent.succeeded":
        print("💰 Payment received!")
        print(data_object)
        StripeIntent.objects.filter(intent_id=data_object["id"]).update(
            status=data_object["status"],
            payment_method_id=data_object["payment_method"],
        )
    elif event_type == "payment_intent.payment_failed":
        print("❌ Payment failed.")
        print(data_object)
        StripeIntent.objects.filter(intent_id=data_object["id"]).update(
            status=data_object["status"],
            payment_method_id=data_object["payment_method"],
        )
    return JsonResponse({"status": "success", "message": "message"})


@csrf_exempt
def paypal_webhook_callback(request):
    try:
        if request.method == "POST":
            request_data = json.loads(request.body)
            event = request_data.get("event_type")
            if event == "CHECKOUT.ORDER.APPROVED":
                order_id = request_data["resource"]["id"]
                order_status = request_data["resource"]["status"]
                PayPalOrder.objects.filter(order_id=order_id).update(
                    status=order_status
                )
            elif event == "PAYMENT.CAPTURE.COMPLETED":
                order_id = request_data["supplementary_data"]["related_ids"]["order_id"]
                order_status = request_data["resource"]["status"]
                PayPalOrder.objects.filter(order_id=order_id).update(
                    status=order_status
                )
            return JsonResponse(
                data={"status": "success", "message": "Event received"},
                status=status.HTTP_200_OK,
            )
        else:
            return JsonResponse(
                data={"status": "error", "message": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        print(e, traceback.print_exc())
        return JsonResponse(
            data={"status": "error", "message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@login_required
def stripe_paypal_test_paymnet(request):
    return render(
        request=request,
        template_name="card.html",
        context={"user": request.user, "paypal_client_id": PayPal.get_client_id()},
    )
