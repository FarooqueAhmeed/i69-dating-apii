from django.core.management.base import BaseCommand
from django.core.management import call_command

from chat.models import FirstMessage, Broadcast

from gifts.models import Gift


class Command(BaseCommand):
    def handle(self, *args, **options):
        # generate default pickers and generate translations
        call_command("set_default_pickers")
        # generate translations for broadcast
        for broadcast in Broadcast.objects.all():
            broadcast.save()
        # generate transaltions for firstmessage
        for firstmessage in FirstMessage.objects.all():
            firstmessage.save()

        # generate translations for gifts
        for gift in Gift.objects.all():
            gift.save()
