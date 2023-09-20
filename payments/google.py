from .models import GoogleOrder


class Google(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def create_order(cls, amount: float, currency: str = "USD", user=None, order_id=None, status=None):
        print("Google.create_order")
        print(amount, currency, user, order_id, status)
        response = GoogleOrder.objects.create(
            user=user,
            order_id=order_id,
            status=status,
            amount=amount,
            currency=currency,
        )
        if response:
            return response
        else:
            return None
