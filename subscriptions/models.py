from django.db import models

from framework import settings


class SubscriptionsPlan(models.Model):

    name = models.CharField(max_length=95)

    def __str__(self):
        return self.name


class ModeratorSubscriptionPlan(models.Model):
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_subscription")
    subscription = models.ForeignKey(SubscriptionsPlan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.moderator.email} is following subscription plan {self.subscription.name}"
