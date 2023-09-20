import googletrans
import graphene
from django.contrib.auth import get_user_model
from googletrans import Translator
from graphene_file_upload.scalars import Upload

from .models import StockImage
from .serializer import StockImageType

from user.utils import translate_error_message

translator = Translator()
lg = googletrans.LANGUAGES

User = get_user_model()


class StockImageMutation(graphene.Mutation):
    class Arguments:
        moderator_id = graphene.String(required=True)
        file = Upload(required=True)

    stock_image = graphene.Field(StockImageType)

    @classmethod
    def mutate(cls, root, info, file, moderator_id):

        muser = info.context.user
        moderator = User.objects.filter(id=moderator_id).first()

        if not moderator:
            return Exception(translate_error_message(info.context.user, "Invalid moderator id"))

        if not muser.roles.filter(role__in=["ADMIN"]).exists():
            return Exception(translate_error_message(info.context.user, "You cant perform this action"))

        new_stock_image = StockImage(
            user=moderator,
            file=file,
        )
        new_stock_image.save()

        return StockImageMutation(stock_image=new_stock_image)


class DeleteStockImageMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):

        user = info.context.user
        image = StockImage.objects.filter(id=id).first()

        if not image:
            return Exception(translate_error_message(info.context.user, "Invalid image id"))

        if not user.roles.filter(role__in=["ADMIN"]).exists():
            return Exception(translate_error_message(info.context.user, "You cant perform this action"))

        image.delete()

        return DeleteStockImageMutation(success=True)


class Mutation(graphene.ObjectType):
    upload_stock_image = StockImageMutation.Field()
    delete_stock_image = DeleteStockImageMutation.Field()


class Query(graphene.ObjectType):
    stock_images = graphene.List(StockImageType, user_id=graphene.String(required=True))

    def resolve_stock_images(self, info, user_id, **kwargs):
        return StockImage.objects.filter(user__id=user_id)
