from celery import shared_task
from django.utils import timezone
from chat.models import Notification, send_notification_fcm

from .models import PackagePurchase


@shared_task(name="check_subscriptions")
def check_subscriptions(*args, **kwargs):
    expired_subscriptions = PackagePurchase.objects.filter(
        is_active=True, ends_at__lt=timezone.now()
    )
    expired_subscriptions.update(is_active=False)
    print("EXPIRED SUBSCRIPTIONS MARKED IN ACTIVE")


@shared_task(name="alert_subscriptions")
def alert_subscriptions(*args, **kwargs):
    date = timezone.now().date()
    week_alert = date + timezone.timedelta(days=2)
    month_alert = date + timezone.timedelta(days=5)
    three_month_alert = date + timezone.timedelta(days=7)
    six_month_alert = date + timezone.timedelta(days=10)
    year_alert = date + timezone.timedelta(days=10)
    week_subscriptions = PackagePurchase.objects.filter(
        is_active=True, plan__validity="PERWEEK", ends_at__date=week_alert
    )
    month_subscriptions = PackagePurchase.objects.filter(
        is_active=True, plan__validity="PERMONTH", ends_at__date=month_alert
    )
    three_month_subscriptions = PackagePurchase.objects.filter(
        is_active=True, plan__validity="PER3MONTH", ends_at__date=three_month_alert
    )
    six_month_subscriptions = PackagePurchase.objects.filter(
        is_active=True, plan__validity="PER6MONTH", ends_at__date=six_month_alert
    )
    year_subscriptions = PackagePurchase.objects.filter(
        is_active=True, plan__validity="PERYEAR", ends_at__date=year_alert
    )
    subscriptions_alert = (
        week_subscriptions
        | month_subscriptions
        | three_month_subscriptions
        | six_month_subscriptions
        | year_subscriptions
    )

    remaining_days = {
        "PERWEEK": 2,
        "PERMONTH": 5,
        "PER3MONTH": 7,
        "PER6MONTH": 10,
        "PERYEAR": 10,
    }
    notification_setting = "MSGREMINDER"

    for alert in subscriptions_alert:
        notification_obj = Notification(
            user_id=alert.user.id, notification_setting_id=notification_setting, data={}
        )
        send_notification_fcm(
            notification_obj=notification_obj,
            remaining_days=f"Your subscription is about to expire in {remaining_days[alert.plan.validity]} days",
        )
    print("ALERTS SENT")


@shared_task()
def check_package_task(username):
    print(f"Task Completed: {username}")
