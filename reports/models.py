from django.db import models
import datetime

from django.utils.timezone import now

# Create your models here.


class Reported_Users(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Reporter and Reportee can be null for backwards compatibility
    reporter = models.ForeignKey(
        "user.User", related_name="reported_list", on_delete=models.SET_NULL, null=True
    )
    reportee = models.ForeignKey(
        "user.User", related_name="reports", on_delete=models.SET_NULL, null=True
    )
    reason = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Reported Users"
        verbose_name = "Reported Users"

    def __str__(self):
        return (
            str(self.reporter)
            + " - "
            + str(self.reportee)
            + " ---- "
            + str(self.timestamp)
        )


class GoogleAuth(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    email = models.EmailField(null=True, blank=True)
    sub = models.CharField(max_length=200, null=True, blank=True)


class SocialAuthDetail(models.Model):
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'
    STATUS_CHOICES = (
        (ENABLED, 'ENABLED'),
        (DISABLED, 'DISABLED'),
    )
    id = models.BigAutoField(primary_key=True, null=False)
    provider = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ENABLED)
    updated_by = models.ForeignKey(
        "user.User", related_name="auth_updated_by", on_delete=models.SET_NULL, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.provider