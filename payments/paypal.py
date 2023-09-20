import base64
import json

import requests

from .models import PrivateKey, PublicKey


class PayPal(object):
    def __init__(self) -> None:
        pass

    env = "test"  # test or live

    @classmethod
    def get_base_uri(cls):
        return "https://api-m.paypal.com"

        # if cls.env == "test":
        #     return "https://api.sandbox.paypal.com"
        # else:
        #   return "https://api-m.paypal.com"

    @classmethod
    def get_client_id(cls):
        key = PublicKey.objects.filter(payment_gateway="paypal").first()
        if key:
            return key.key_text
        return None

    @classmethod
    def get_client_secret(cls):
        key = PrivateKey.objects.filter(payment_gateway="paypal").first()
        if key:
            return key.key_text
        return None

    @classmethod
    def get_token(cls) -> str:
        try:
            resposne = requests.post(
                url=f"{cls.get_base_uri()}/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {base64.b64encode((cls.get_client_id() + ':' + cls.get_client_secret()).encode()).decode()}",
                },
            )
            return json.loads(resposne.text)["access_token"]

        except Exception as e:
            return None

    @classmethod
    def create_order(cls, amount: float, currency: str = "USD") -> dict:
        token = cls.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        url = f"{cls.get_base_uri()}/v2/checkout/orders"
        body = {
            "intent": "CAPTURE",
            "application_context": {
                "brand_name": "iSixtyNine",
                "shipping_preference": "NO_SHIPPING",
            },
            "purchase_units": [
                {
                    "reference_id": "iSixtyNine-COINS",
                    "description": "Purchase Coins",
                    "custom_id": "Purchase Coins",
                    "soft_descriptor": "Purchase Coins",
                    "amount": {
                        "currency_code": currency,
                        "value": f"{amount:.2f}",
                        "breakdown": {
                            "item_total": {
                                "currency_code": currency,
                                "value": f"{amount:.2f}",
                            },
                        },
                    },
                    "items": [
                        {
                            "name": "i69 COINS",
                            "description": "Purchase Coins",
                            "sku": "i69-coins",
                            "unit_amount": {
                                "currency_code": currency,
                                "value": f"{amount:.2f}",
                            },
                            "quantity": "1",
                        }
                    ],
                }
            ],
            "note_to_payer": "Contact us at contact@i69app.com for any questions on your order.",
        }
        result = requests.post(url, json=body, headers=headers)

        return result.json()

    @classmethod
    def capture_order_payment(cls, order_id) -> dict:
        token = cls.get_token()
        response = requests.post(
            url=f"{cls.get_base_uri()}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={},
        )
        return response
