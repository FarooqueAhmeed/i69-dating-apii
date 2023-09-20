from django.urls import path

from payments import views

urlpatterns = [
    path("webhook/boku/authorisation/", views.boku_pin_authorisation_callback),
    path("webhook/boku/charge/", views.boku_charge_payment_callback),
    path("webhook/boku/refund/", views.boku_refund_payment_callback),
    path("webhook/stripe/", views.stripe_webhook_callback, name="stripe-webhook"),
    path("webhook/paypal/", views.paypal_webhook_callback, name="paypal-webhook"),
    path("test-payment/", views.stripe_paypal_test_paymnet, name="payment-test"),
]
