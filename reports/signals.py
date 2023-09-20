from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Reported_Users
from user.utils import get_recipients_of_admin_realtime_notification


def reported_users_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    description = f"ID:{instance.id} | Reporter: {instance.reporter} | Reportee: {instance.reportee}"
    notify.send(instance, recipient=recipients, verb='An user was reported', description=description, event_type='REPORT_USER')

post_save.connect(reported_users_handler, sender=Reported_Users)
