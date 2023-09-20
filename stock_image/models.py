from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class StockImage(models.Model):
    def get_avatar_path(self, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "static/uploads/stock_images/" + filename

    user = models.ForeignKey(
        User, related_name="stock_images", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to=get_avatar_path, null=True, blank=True, max_length=1000
    )

    def __str__(self):
        return str(self.id)
