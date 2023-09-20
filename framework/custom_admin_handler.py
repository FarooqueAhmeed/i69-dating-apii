from django.utils.log import AdminEmailHandler
from notifications.signals import notify

class CustomAdminHandler(AdminEmailHandler):
   def send_mail(self, subject, message, *args, **kwargs):
      pos = message.find('Django Version')
      from user.utils import get_recipients_of_admin_realtime_notification
      recipients = get_recipients_of_admin_realtime_notification()
      for recipient in recipients:
         notify.send(recipient, recipient=recipient, verb=subject, description=message[:pos], event_type='SERVER_ERROR')
