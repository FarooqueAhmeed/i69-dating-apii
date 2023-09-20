from celery import shared_task

from payments.boku import Boku
from payments import models

import pycountry


@shared_task(name="sync_boku_operators")
def sync_boku_operators(*args, **kwargs):
    """
    Celery Task for syncing the boku supported operator
    data
    """

    boku = Boku()

    url = "https://api-jwt.fortumo.io/capabilities/162350b61495c7d69dcc6a63973ae75f/"

    data = boku.make_get_request(url=url)

    for country_data in data:
        country = pycountry.countries.get(alpha_2=country_data["country"])

        for payment_method in country_data["payment_methods"]:
            if payment_method["name"] == "CARRIER_BILLING":
                for channel in payment_method["channel"]:
                    operator_name = channel["name"]
                    operator_code = channel["code"]
                    max_transaction_limit = channel["transaction_ranges"][0]["max"]
                    currency = channel["transaction_ranges"][0]["currency"]

                    operator, created = models.Operator.objects.get_or_create(
                        name=operator_name,
                        code=operator_code,
                        country=country.name,
                        country_id=country.alpha_2,
                        max_transaction_limit=max_transaction_limit,
                    )

                    operator.currency = currency
                    operator.save()

                    if channel.get("msisdn_patterns", None):
                        for msisdn in channel["msisdn_patterns"]:
                            models.Msdin.objects.create(
                                operator=operator, pattern=msisdn
                            )
