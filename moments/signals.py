from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Report, StoryReport
from user.utils import get_recipients_of_admin_realtime_notification


def moment_report_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    description = f"ID:{instance.id} | Reporter: {instance.user} | Report msg: {instance.Report_msg}"
    notify.send(instance, recipient=recipients, verb='A moment was reported', description=description, event_type='REPORT_MOMENT')

def story_report_handler(sender, instance, created, **kwargs):
    recipients = get_recipients_of_admin_realtime_notification()
    description = f"ID:{instance.id} | Reporter: {instance.user} | Report msg: {instance.Report_msg}"
    notify.send(instance, recipient=recipients, verb='A story was reported', description=description, event_type='REPORT_STORY')

post_save.connect(moment_report_handler, sender=Report)
post_save.connect(story_report_handler, sender=StoryReport)
