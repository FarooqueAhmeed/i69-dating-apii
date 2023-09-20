import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import (
    Gift,
    AllGifts,
    Giftpurchase,
    GiftPurchaseMessageText,
    AbstractGift,
    RealGift,
    VirtualGift,
    RealGiftPriceForRegion,
    VirtualGiftPriceForRegion
)
from user.models import User
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
import django_filters
from django.core.files import File
from user.schema import UserPhotoType
from datetime import datetime
from graphene_file_upload.scalars import Upload
from django.db.models import F, Q
from chat.models import (
    Notification,
    send_notification_fcm,
    Room,
    Message,
    ChatMessageImages,
)
from defaultPicker.utils import translated_field_name, custom_translate
from .utils import get_gift
from user.models import ChatsQue
from chat.schema import OnNewMessage
from user.utils import translate_error_message


class GiftType1(DjangoObjectType):
    url = graphene.String()

    class Meta:
        model = AllGifts
        fields = "__all__"

    def resolve_url(self, info):
        return self.picture.url

    def resolve_gift_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "gift_name"))


class RealGiftType(DjangoObjectType):
    url = graphene.String()
    type = graphene.String()
    cost = graphene.Float()

    class Meta:
        model = RealGift
        fields = "__all__"

    def resolve_url(self, info):
        return self.picture.url

    def resolve_gift_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "gift_name"))

    def resolve_id(self, info):
        return self.allgift.id

    def resolve_type(self, info):
        return "real"

    def resolve_cost(self, info):
        user_region = info.context.user.get_coinsettings_region()
        gift_cost = self.cost
        if user_region:
            gift_price_for_region = RealGiftPriceForRegion.objects.filter(real_gift=self.id, region=user_region).first()
            gift_cost = gift_price_for_region.cost
        return gift_cost


class VirtualGiftType(DjangoObjectType):
    url = graphene.String()
    type = graphene.String()
    cost = graphene.Float()

    class Meta:
        model = VirtualGift
        fields = "__all__"

    def resolve_url(self, info):
        return self.picture.url

    def resolve_gift_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "gift_name"))

    def resolve_id(self, info):
        return self.allgift.id

    def resolve_type(self, info):
        return "virtual"

    def resolve_cost(self, info):
        user_region = info.context.user.get_coinsettings_region()
        gift_cost = self.cost
        if user_region:
            gift_price_for_region = VirtualGiftPriceForRegion.objects.filter(virtual_gift=self.id,
                                                                             region=user_region).first()
            if gift_price_for_region:
                gift_cost = gift_price_for_region.cost
        return gift_cost


class UserType2(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)

    avatar = graphene.Field(UserPhotoType)

    def resolve_avatar(self, info):
        return self.avatar()


class GiftDetailType(DjangoObjectType):
    gift_name = graphene.String()
    cost = graphene.Float()
    picture = graphene.String()
    url = graphene.String()
    status = graphene.String()

    class Meta:
        model = AllGifts
        fields = "__all__"

    def resolve_gift_name(self, info):
        gift = get_gift(self, info)
        return getattr(gift, translated_field_name(info.context.user, "gift_name"))

    def resolve_cost(self, info):
        gift = get_gift(self, info)
        return gift.cost if gift else 0

    def resolve_picture(self, info):
        gift = get_gift(self, info)
        return gift.picture if gift else ""

    def resolve_url(self, info):
        gift = get_gift(self, info)
        return gift.picture.url if gift.picture else ""


class GiftpurchaseType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    gift = graphene.Field(GiftDetailType)

    class Meta:
        model = Giftpurchase
        fields = "__all__"
        filter_fields = {"user__id": ["exact"], "receiver__id": ["exact"]}
        interfaces = (relay.Node,)

    # @property
    # def qs(self):
    #     # The query context can be found in self.request.
    #     return super(GiftpurchaseType, self).qs.order_by("purchased_on")


class GiftpurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = Giftpurchase
        fields = ("user__id", "gift", "receiver__id", "purchased_on")
        # order_by = django_filters.OrderingFilter(fields=(("-purchased_on")))
        order_by = (
            "-purchased_on",
            "id",
        )


class Creategiftmutation(graphene.Mutation):
    class Arguments:
        gift_name = graphene.String(required=True)
        type = graphene.String(required=True)
        cost = graphene.Float(required=True)
        picture = Upload(required=True)

    gift = graphene.Field(GiftType1)

    @classmethod
    def mutate(cls, root, info, gift_name, type, cost, picture):
        new_obj = Gift.objects.create(
            gift_name=gift_name, type=type, cost=cost, picture=picture
        )
        new_obj.save()
        return Creategiftmutation(gift=new_obj)


class Deletegiftmutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    gift = graphene.Field(GiftType1)
    msg = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        del_obj = Gift.objects.filter(id=id).first()
        if del_obj:
            del_obj.delete()
            return  # Deletegiftmutation(msg="Gift has been deleted.")
        else:
            return GraphQLError(
                "There is no particular gift avaible in gift table with this ID"
            )


class Updategiftmutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        gift_name = graphene.String(required=True)
        type = graphene.String(required=True)
        cost = graphene.Float(required=True)
        picture = Upload(required=True)

    error = graphene.Boolean()
    msg = graphene.String()
    gift = graphene.Field(GiftType1)

    @classmethod
    def mutate(cls, root, info, id, gift_name, type, cost, picture):
        new_obj = Gift.objects.filter(id=id).first()
        if new_obj:
            new_obj.gift_name = gift_name
            new_obj.type = type
            new_obj.cost = cost
            new_obj.picture = picture
            new_obj.save()
            return Creategiftmutation(gift=new_obj)
        else:
            return GraphQLError(
                "There is no particular gift avaible in gift table with this ID"
            )


class Purchasegiftmutation(graphene.Mutation):
    class Arguments:
        gift_id = graphene.ID()
        receiver_id = graphene.ID()
        sender_id = graphene.ID()

    error = graphene.Boolean()
    msg = graphene.String()
    gift_purchase = graphene.Field(GiftpurchaseType)

    @classmethod
    def mutate(cls, root, info, gift_id, receiver_id, sender_id):
        user_obj = info.context.user
        if sender_id:
            user_obj = User.objects.filter(id=sender_id).first()

        if user_obj:
            receiver_obj = User.objects.filter(id=receiver_id).first()

            if receiver_obj:
                if receiver_obj == user_obj:
                    raise Exception(
                        translate_error_message(info.context.user, "You cannot gift yourself")
                    )

                allgift = AllGifts.objects.filter(id=gift_id).first()
                allgift_type = allgift.type if allgift else None

                user_region = user_obj.get_coinsettings_region()

                if allgift_type == "real":
                    gift_obj = RealGift.objects.filter(allgift__id=gift_id).first()
                    if user_region:
                        gift_price_for_region = RealGiftPriceForRegion.objects.filter(real_gift=gift_obj,
                                                                                      region=user_region).first()
                        gift_obj.cost = gift_price_for_region.cost
                elif allgift_type == "virtual":
                    gift_obj = VirtualGift.objects.filter(allgift__id=gift_id).first()
                    if user_region:
                        gift_price_for_region = VirtualGiftPriceForRegion.objects.filter(virtual_gift=gift_obj,
                                                                                         region=user_region).first()
                        gift_obj.cost = gift_price_for_region.cost
                else:
                    gift_obj = None

                print("GIFT", str(gift_obj))
                if gift_obj:
                    if allgift_type == "virtual" and user_obj.roles.filter(Q(role__in=["MODERATOR"])).exists():
                        print("Coins should not be deducted from Moderator user")
                        user_obj.save()
                    elif allgift_type == "real" and user_obj.roles.filter(Q(role__in=["MODERATOR"])).exists():
                        raise Exception(
                            translate_error_message(info.context.user, "Moderator User cannot send Real Gifts")
                        )
                    else:
                        user_obj.deductCoins(gift_obj.cost, "Gift purchase")
                        user_obj.save()
                    receiver_obj.gift_coins = int(
                        receiver_obj.gift_coins + gift_obj.cost
                    )
                    receiver_obj.gift_coins_date = datetime.now()
                    receiver_obj.save()
                    gift_purchase_obj = Giftpurchase(
                        user=user_obj, gift=allgift, receiver_id=receiver_id
                    )
                    gift_purchase_obj.save()
                    notification_obj = Notification(
                        sender=user_obj,
                        user=receiver_obj,
                        notification_setting_id="GIFT RLVRTL",
                    )
                    # data = {'coins': str(coins)}
                    # notification_obj.data=data

                    # ----------------- Creating or geting ChatRoom
                    room_name_a = [user_obj.username, receiver_obj.username]
                    room_name_a.sort()
                    room_name_str = room_name_a[0] + "_" + room_name_a[1]

                    try:
                        chat_room = Room.objects.get(name=room_name_str)
                    except Room.DoesNotExist:
                        chat_room = Room(
                            name=room_name_str, user_id=user_obj, target=receiver_obj
                        )
                        chat_room.save()

                    if user_obj == chat_room.user_id:
                        user_for_notification = chat_room.target

                    if user_obj == chat_room.target:
                        user_for_notification = chat_room.user_id
                    # ----------------- Sending message
                    # message = Message(
                    #     room_id=chat_room,
                    #     user_id=user_obj,
                    #     content=f"Sent {gift_obj.gift_name} gift of {gift_obj.cost} coins.",
                    # )
                    # message.save()

                    chat_room.last_modified = datetime.now()
                    chat_room.save()

                    # ----------------- Sending message notification
                    # notification_setting="SNDMSG"
                    # app_url=None
                    # priority=None
                    # icon=None
                    # avatar_url = None
                    # # checks for avatar_url if None
                    # try:
                    #     avatar_url = user_obj.avatar().file.url
                    # except:
                    #     avatar_url=None
                    # data={
                    #     "roomID":chat_room.id,
                    #     "notification_type":notification_setting,
                    #     "message":message.content,
                    #     "user_avatar":avatar_url,
                    #     "title":"Sent Gift",
                    #     "giftUrl":None,
                    #     "giftID": gift_id
                    # }
                    # if gift_obj.picture:
                    #     data['giftUrl']=gift_obj.picture.url

                    # if avatar_url:
                    #     icon=info.context.build_absolute_uri(avatar_url)
                    # android_channel_id=None
                    # notification_obj=Notification(user=receiver_obj, sender=user_obj, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
                    # send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)
                    # OnNewMessage.broadcast(payload=message, group=str(receiver_obj.id))
                    # OnNewMessage.broadcast(payload=message, group=str(chat_room.user_id.id))

                    # try:
                    #     send_notification_fcm(notification_obj)
                    # except Exception as e:
                    #     raise Exception(str(e))

                    # ----------------- Sending message on receiver side
                    if gift_obj.picture:
                        giftUrl = info.context.build_absolute_uri(gift_obj.picture.url)
                    g = ChatMessageImages()
                    g.image.save(
                        gift_obj.picture.name, File(gift_obj.picture.file), save=True
                    )
                    g.upload_type = "image"
                    g.save()

                    gift_message = GiftPurchaseMessageText.objects.last().generate_text(
                        gift_name=gift_obj.gift_name, coins=(gift_obj.cost)
                    )

                    message = Message(
                        room_id=chat_room,
                        user_id=receiver_obj,
                        content=f"{info.context.build_absolute_uri(g.image.url)} {gift_message}",
                        message_type="G",
                        gift_message_sender=user_obj,
                    )
                    message.save()

                    chat_room.last_modified = datetime.now()
                    chat_room.save()

                    current_user = info.context.user
                    if current_user.roles.filter(role__in=["MODERATOR", "CHATTER"]):
                        message.sender_worker = current_user
                        message.save()
                        chatque = ChatsQue.objects.filter(room_id=chat_room.id)
                        if chatque.count() > 0:
                            chatque[0].moderator.owned_by.remove(current_user)
                            chatque[0].delete()

                    # ----------------- Sending message notification on receiver side

                    notification_setting = "SNDMSG"
                    app_url = None
                    priority = None
                    icon = None
                    avatar_url = None
                    # checks for avatar_url if None
                    try:
                        avatar_url = receiver_obj.avatar().file.url
                    except:
                        avatar_url = None
                    data = {
                        "roomID": chat_room.id,
                        "notification_type": notification_setting,
                        "message": message.content,
                        "user_avatar": avatar_url,
                        "title": "Received Gift",
                        "giftUrl": None,
                    }
                    if gift_obj.picture:
                        data["giftUrl"] = gift_obj.picture.url

                    if avatar_url:
                        icon = info.context.build_absolute_uri(avatar_url)
                    android_channel_id = None
                    notification_obj = Notification(
                        user=receiver_obj,
                        sender=user_obj,
                        app_url=app_url,
                        notification_setting_id=notification_setting,
                        data=data,
                        priority=priority,
                    )
                    send_notification_fcm(
                        notification_obj=notification_obj,
                        android_channel_id=android_channel_id,
                        giftUrl=info.context.build_absolute_uri(gift_obj.picture.url),
                    )

                    OnNewMessage.broadcast(payload=message, group=str(chat_room.id))
                    # OnNewMessage.broadcast(payload=message, group=str(user_for_notification.id))

                    # try:
                    #     send_notification_fcm(notification_obj)
                    # except Exception as e:
                    #     raise Exception(str(e))
                    return Purchasegiftmutation(
                        gift_purchase=gift_purchase_obj, msg="", error=False
                    )

                else:
                    return Purchasegiftmutation(
                        gift_purchase=None,
                        msg=custom_translate(
                            info.context.user, "Gift not exist for particular gift id"
                        ),
                        error=True,
                    )
            else:
                return Purchasegiftmutation(
                    gift_purchase=None,
                    msg=custom_translate(info.context.user, "receiver does not exist"),
                    error=True,
                )
        else:
            return Purchasegiftmutation(
                gift_purchase=None,
                msg=custom_translate(
                    info.context.user, "You need to log in first of all "
                ),
                error=True,
            )


# class Currentuseriftmutation(graphene.Mutation):
#     class Arguments:
#         gift_id=graphene.ID()
#         receiver_id=graphene.ID()

#     gift_purchase=graphene.Field(GiftpurchaseType)

#     @classmethod
#     def mutate(cls, root, info,gift_id,receiver_id):
#         user_obj=User.objects.filter(id=info.context.user.id).first()
#         receiver_obj=User.objects.filter(id=receiver_id).first()
#         gift_obj=Gift.objects.filter(id=gift_id).first()
#         if user_obj.purchase_coins>=gift_obj.cost:
#             user_obj.purchase_coins=int(user_obj.purchase_coins-gift_obj.cost)
#             user_obj.save()
#             receiver_obj.gift_coins=int(receiver_obj.gift_coins+gift_obj.cost)
#             receiver_obj.save()
#             gift_purchase_obj=Giftpurchase(user_id=info.context.user.id,gift_id=gift_id,receiver_id=receiver_id)
#             gift_purchase_obj.save()
#             return Purchasegiftmutation(gift_purchase=gift_purchase_obj)
#         else:
#             return GraphQLError("not sufficient coin avaiable in user account")


class Mutation(graphene.ObjectType):
    create_gift = Creategiftmutation.Field()
    delete_gift = Deletegiftmutation.Field()
    update_gift = Updategiftmutation.Field()
    gift_purchase = Purchasegiftmutation.Field()

    # current_user_gift=Currentuseriftmutation.Field()


class Query(graphene.ObjectType):
    all_gift = graphene.List(GiftType1)
    all_user_gifts = DjangoFilterConnectionField(
        GiftpurchaseType, filterset_class=GiftpurchaseFilter
    )
    all_real_gift = graphene.List(RealGiftType)
    all_virtual_gift = graphene.List(VirtualGiftType)

    def resolve_all_real_gift(root, info):
        user = info.context.user
        user_region = user.get_coinsettings_region()
        real_gifts = list(RealGift.objects.filter(status="ACTIVE").all())
        if not user_region:
            return real_gifts
        else:
            for real_gift in real_gifts:
                real_gifts_regional_price = (RealGiftPriceForRegion.objects.filter
                                             (region_id=user_region, real_gift_id=real_gift.id)).first()
                if real_gifts_regional_price:
                    real_gift.cost = real_gifts_regional_price.cost
            return real_gifts

    def resolve_all_virtual_gift(root, info):
        user = info.context.user
        user_region = user.get_coinsettings_region()
        virtual_gifts = list(VirtualGift.objects.filter(status="ACTIVE").all())
        if not user_region:
            return virtual_gifts
        else:
            for virtual_gift in virtual_gifts:
                virtual_gifts_regional_price = (VirtualGiftPriceForRegion.objects.filter
                                                (region_id=user_region, virtual_gift_id=virtual_gift.id)).first()
                if virtual_gifts_regional_price:
                    virtual_gift.cost = virtual_gifts_regional_price.cost
            return virtual_gifts

    def resolve_all_gift(root, info):
        return Gift.objects.all()

    def resolve_all_user_gifts(root, info, user__id=None, receiver__id=None, **kwargs):
        if user__id and not receiver__id:
            return Giftpurchase.objects.filter(user=user__id).order_by("-purchased_on")
        if not user__id and receiver__id:
            return Giftpurchase.objects.filter(receiver=receiver__id).order_by(
                "-purchased_on"
            )
        if user__id and receiver__id:
            return Giftpurchase.objects.filter(
                user=user__id, receiver=receiver__id
            ).order_by("-purchased_on")
