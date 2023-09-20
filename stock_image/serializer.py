from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from .models import StockImage

User = get_user_model()


class StockImageType(DjangoObjectType):
    class Meta:
        model = StockImage
        fields = ["id", "file", "created_date"]

    def resolve_file(self, info):
        return info.context.build_absolute_uri(self.file.url)
