# Create your views here.
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PaypalFormView(FormView):
    permission_classes = [IsAuthenticated]

    template_name = "paypal_form.html"
    form_class = PayPalPaymentsForm

    def get_initial(self):
        return {
            "business": "your-paypal-business-address@example.com",
            "amount": 20,
            "currency_code": "EUR",
            "item_name": "Example",
            "invoice": 1234,
            "notify_url": self.request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": self.request.build_absolute_uri(reverse("paypal-return")),
            "cancel_return": self.request.build_absolute_uri(reverse("paypal-cancel")),
            "lc": "EN",
            "no_shipping": "1",
        }


class PaymentDone(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"status": "done"})


class PaymentCancel(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"status": "cancelled"})
