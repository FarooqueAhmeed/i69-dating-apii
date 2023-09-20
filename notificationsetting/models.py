from django.db import models
# Create your models here.


class NotificationSound(models.Model):
    SOUND_CHOICES = (
        ("coin_purchase", "Coin Purchase"),
        ("package_purchase", "Package Purchase"),
        ("gift_purchase", "Gift Purchase"),
        ("new_user", "New User"),
        ("report_user", "Report User"),
        ("report_moment", "Report Moment"),
        ("notification", "Notification"),
        ("server_error", "Server Error"),
    )

    name = models.CharField(max_length=255, choices=SOUND_CHOICES, unique=True)
    file = models.FileField(upload_to='admin/sound/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
