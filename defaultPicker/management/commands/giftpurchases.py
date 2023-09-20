from django.core.management.base import BaseCommand
from django.core.management import call_command

from user.models import UserLimit
from gifts.models import GiftPurchaseMessageText, Giftpurchase


class Command(BaseCommand):
    def handle(self, *args, **options):
        # generate default pickers and generate translations
        Giftpurchase.objects.all().delete()
