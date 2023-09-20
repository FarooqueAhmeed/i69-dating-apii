from django.db.models.signals import post_save
from notifications.signals import notify
from .models import User, HideUserInterestedIn, UserProfileTranlations, UserInterestForRegion
from .utils import get_recipients_of_admin_realtime_notification
from .schema import HideInterestedInSubscription, UserProfileTranslationSubscription

def new_user_handler(sender, instance, created, **kwargs):
    if created:
        recipients = get_recipients_of_admin_realtime_notification()
        description = f"ID:{instance.id} | Email: {instance.email}"
        notify.send(instance, recipient=recipients, verb='A new user has joined', description=description, event_type='NEW_USER')

post_save.connect(new_user_handler, sender=User)


def hide_interested_in_handler(sender, instance, created, **kwargs):
    if created:
        HideInterestedInSubscription.broadcast(
            group='hide_interested_in_subscription',
            payload={'user_interestedIn_instance': instance}
        )

def update_hide_interested_in_handler(sender, instance, **kwargs):
    HideInterestedInSubscription.broadcast(
        group='hide_interested_in_subscription',
        payload={'user_interestedIn_instance': instance}
    )

post_save.connect(hide_interested_in_handler, sender=UserInterestForRegion)
post_save.connect(update_hide_interested_in_handler, sender=UserInterestForRegion)


def add_user_profile_translation_handler(sender, instance, created, **kwargs):
    if created:
        UserProfileTranslationSubscription.broadcast(
            group='user_profile_translation_subscription',
            payload={'user_profile_translation_instance': instance}
        )


def update_user_profile_translation_handler(sender, instance, **kwargs):
    UserProfileTranslationSubscription.broadcast(
        group='user_profile_translation_subscription',
        payload={'user_profile_translation_instance': instance}
    )

post_save.connect(add_user_profile_translation_handler, sender=UserProfileTranlations)
post_save.connect(update_user_profile_translation_handler, sender=UserProfileTranlations)