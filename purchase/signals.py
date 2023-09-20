from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Purchase, PackagePurchase
from user.utils import get_recipients_of_admin_realtime_notification


def coin_purchase_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    description = f"ID:{instance.purchase_id} | Coins purchased: {instance.coins} | Purchased by: {instance.user}"
    notify.send(instance, recipient=recipients, verb='Coins were purchased', description=description, event_type='COIN_PURCHASE')

def package_purchase_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    description = f"ID: {instance.id} | Package: {instance.package} | Plan: {instance.plan} | Purchased by: {instance.user}"
    notify.send(instance, recipient=recipients, verb='A package was purchased', description=description, event_type='PACKAGE_PURCHASE')


post_save.connect(coin_purchase_handler, sender=Purchase)
post_save.connect(package_purchase_handler, sender=PackagePurchase)
