from django.db import models


class WorkerInvitation(models.Model):
    email = models.EmailField()
    token = models.UUIDField()
    is_admin_permission = models.BooleanField()
    is_chat_admin_permission = models.BooleanField()

    def __str__(self):
        return self.email


class EmailSettings(models.Model):
    email_host = models.CharField(max_length=255)
    email_port = models.PositiveIntegerField()
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)
    email_use_tls = models.BooleanField(default=True)
    default_from_email = models.CharField(max_length=255)

    def __str__(self):
        return self.default_from_email

    class Meta:
        verbose_name_plural = 'Email settings'
