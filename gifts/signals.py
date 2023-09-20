from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Giftpurchase, RealGift, VirtualGift
from user.models import User
from user.utils import get_recipients_of_admin_realtime_notification


def gift_purchase_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    gift = instance    
    if instance.gift.type == "real":
        gift = RealGift.objects.get(allgift=instance.gift.id)
    else:
        gift = VirtualGift.objects.get(allgift=instance.gift.id)
    gift_name = gift.gift_name    
    verb = f"A {instance.gift.type} gift ({gift_name}) was purchased"
    description = f"ID:{instance.id} | Purchased by: {instance.user} | Purchased for: {instance.receiver}"
    notify.send(instance, recipient=recipients, verb=verb, description=description, event_type='GIFT_PURCHASE')


post_save.connect(gift_purchase_handler, sender=Giftpurchase)
