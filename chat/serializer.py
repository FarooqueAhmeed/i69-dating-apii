import graphene
from django_filters import FilterSet, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType
from django.db.models import Q

from chat.models import *  # Room, Message, Broadcasts
from django.contrib.auth import get_user_model

from user.models import ModeratorQue, ChatsQue, PrivatePhotoViewRequest
from defaultPicker.utils import translated_field_name, custom_translate

import datetime

User = get_user_model()


# class UserFilter(FilterSet):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', "email", "last_name", "first_name", "id",)
#         order_by = ("id",)


class ChatUserType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = User
        fields = ["last_name", "first_name", "username", "email", "id", "isOnline"]
        interfaces = (relay.Node,)


class ModeratorQueueType(DjangoObjectType):
    class Meta:
        model = ModeratorQue


class ChatQueueType(DjangoObjectType):
    class Meta:
        model = ChatsQue


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = ("last_modified", "name", "user_id", "target")
        order_by = (
            "-last_modified",
            "id",
        )


class RoomType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)
    unread = graphene.String()
    blocked = graphene.Int()

    class Meta:
        model = Room
        fields = "__all__"
        interfaces = (relay.Node,)


class NoteType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)
    unread = graphene.String()

    class Meta:
        model = Notes
        fields = "__all__"
        interfaces = (relay.Node,)


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = (
            "room_id",
            "user_id",
            "content",
            "read",
            "timestamp",
        )
        order_by = ("-timestamp", "id")


class MessageType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)
    request_status = graphene.String()
    private_photo_request_id = graphene.Int()

    class Meta:
        model = Message
        fields = "__all__"
        interfaces = (relay.Node,)

    def resolve_content(self, info):
        if self.message_type == "G":
            # print(self.id)
            # print(self.gift_message_sender.fullName)
            content = self.content.split(" ")
            image, message = content[0], " ".join(content[1:])
            message = custom_translate(info.context.user, message)
            message = message.replace("{0}", self.gift_message_sender.fullName)
            content = image + " " + message
            return content
        elif self.message_type == "P" or self.message_type == "CM":
            return custom_translate(info.context.user, self.content)

        return self.content

    def resolve_request_status(self, info):
        if self.message_type == "P":
            obj = PrivatePhotoViewRequest.objects.filter(
                id=self.private_photo_request_id
            ).first()
            print(obj)
            return obj.get_status_display()
        else:
            return ""

    def resolve_private_photo_request_id(self, info):
        if self.private_photo_request_id:
            return self.private_photo_request_id
        else:
            return 0


class MessageStatisticsType(graphene.ObjectType):
    day = graphene.Int()
    received_count = graphene.Int()
    sent_count = graphene.Int()


class SameDayMessageStatisticsType(graphene.ObjectType):
    hour = graphene.Int()
    received_count = graphene.Int()
    sent_count = graphene.Int()


# main
class BroadcastType(graphene.ObjectType):
    broadcast_content = graphene.String()
    broadcast_timestamp = graphene.DateTime()
    unread = graphene.String()

    broadcast_content_fr = graphene.String()
    broadcast_content_zh_cn = graphene.String()
    broadcast_content_nl = graphene.String()
    broadcast_content_de = graphene.String()
    broadcast_content_sw = graphene.String()
    broadcast_content_it = graphene.String()
    broadcast_content_ar = graphene.String()
    broadcast_content_iw = graphene.String()
    broadcast_content_ja = graphene.String()
    broadcast_content_ru = graphene.String()
    broadcast_content_fa = graphene.String()
    broadcast_content_pt_br = graphene.String()
    broadcast_content_pt_pt = graphene.String()
    broadcast_content_es = graphene.String()
    broadcast_content_es_419 = graphene.String()
    broadcast_content_el = graphene.String()
    broadcast_content_zh_tw = graphene.String()
    broadcast_content_uk = graphene.String()
    broadcast_content_ko = graphene.String()
    broadcast_content_br = graphene.String()
    broadcast_content_pl = graphene.String()
    broadcast_content_vi = graphene.String()
    broadcast_content_nn = graphene.String()
    broadcast_content_no = graphene.String()
    broadcast_content_sv = graphene.String()
    broadcast_content_hr = graphene.String()
    broadcast_content_cs = graphene.String()
    broadcast_content_da = graphene.String()
    broadcast_content_tl = graphene.String()
    broadcast_content_fi = graphene.String()
    broadcast_content_sl = graphene.String()
    broadcast_content_sq = graphene.String()
    broadcast_content_am = graphene.String()
    broadcast_content_hy = graphene.String()
    broadcast_content_la = graphene.String()
    broadcast_content_lv = graphene.String()
    broadcast_content_th = graphene.String()
    broadcast_content_az = graphene.String()
    broadcast_content_eu = graphene.String()
    broadcast_content_be = graphene.String()
    broadcast_content_bn = graphene.String()
    broadcast_content_bs = graphene.String()
    broadcast_content_bg = graphene.String()
    broadcast_content_km = graphene.String()
    broadcast_content_ca = graphene.String()
    broadcast_content_et = graphene.String()
    broadcast_content_gl = graphene.String()
    broadcast_content_ka = graphene.String()
    broadcast_content_hi = graphene.String()
    broadcast_content_hu = graphene.String()
    broadcast_content_is = graphene.String()
    broadcast_content_id = graphene.String()
    broadcast_content_ga = graphene.String()
    broadcast_content_mk = graphene.String()
    broadcast_content_mn = graphene.String()
    broadcast_content_ne = graphene.String()
    broadcast_content_ro = graphene.String()
    broadcast_content_sr = graphene.String()
    broadcast_content_sk = graphene.String()
    broadcast_content_ta = graphene.String()
    broadcast_content_tg = graphene.String()
    broadcast_content_tr = graphene.String()
    broadcast_content_ur = graphene.String()
    broadcast_content_uz = graphene.String()


# single thread
class BroadcastMsgsFilter(FilterSet):
    class Meta:
        model = Broadcast
        fields = ("by_user_id", "content", "timestamp")
        order_by = ("-timestamp", "id")


class BroadcastMsgsType(DjangoObjectType):
    class Meta:
        model = Broadcast
        fields = "__all__"
        interfaces = (relay.Node,)

    def resolve_content(self, info):
        return getattr(self, translated_field_name(info.context.user, "content"))

    def resolve_timestamp(self, info):
        return info.context.user.date_joined + datetime.timedelta(milliseconds=100)


# main
class FirstMessageType(graphene.ObjectType):
    firstmessage_content = graphene.String()
    firstmessage_timestamp = graphene.DateTime()
    unread = graphene.String()

    firstmessage_content_fr = graphene.String()
    firstmessage_content_zh_cn = graphene.String()
    firstmessage_content_nl = graphene.String()
    firstmessage_content_de = graphene.String()
    firstmessage_content_sw = graphene.String()
    firstmessage_content_it = graphene.String()
    firstmessage_content_ar = graphene.String()
    firstmessage_content_iw = graphene.String()
    firstmessage_content_ja = graphene.String()
    firstmessage_content_ru = graphene.String()
    firstmessage_content_fa = graphene.String()
    firstmessage_content_pt_br = graphene.String()
    firstmessage_content_pt_pt = graphene.String()
    firstmessage_content_es = graphene.String()
    firstmessage_content_es_419 = graphene.String()
    firstmessage_content_el = graphene.String()
    firstmessage_content_zh_tw = graphene.String()
    firstmessage_content_uk = graphene.String()
    firstmessage_content_ko = graphene.String()
    firstmessage_content_br = graphene.String()
    firstmessage_content_pl = graphene.String()
    firstmessage_content_vi = graphene.String()
    firstmessage_content_nn = graphene.String()
    firstmessage_content_no = graphene.String()
    firstmessage_content_sv = graphene.String()
    firstmessage_content_hr = graphene.String()
    firstmessage_content_cs = graphene.String()
    firstmessage_content_da = graphene.String()
    firstmessage_content_tl = graphene.String()
    firstmessage_content_fi = graphene.String()
    firstmessage_content_sl = graphene.String()
    firstmessage_content_sq = graphene.String()
    firstmessage_content_am = graphene.String()
    firstmessage_content_hy = graphene.String()
    firstmessage_content_la = graphene.String()
    firstmessage_content_lv = graphene.String()
    firstmessage_content_th = graphene.String()
    firstmessage_content_az = graphene.String()
    firstmessage_content_eu = graphene.String()
    firstmessage_content_be = graphene.String()
    firstmessage_content_bn = graphene.String()
    firstmessage_content_bs = graphene.String()
    firstmessage_content_bg = graphene.String()
    firstmessage_content_km = graphene.String()
    firstmessage_content_ca = graphene.String()
    firstmessage_content_et = graphene.String()
    firstmessage_content_gl = graphene.String()
    firstmessage_content_ka = graphene.String()
    firstmessage_content_hi = graphene.String()
    firstmessage_content_hu = graphene.String()
    firstmessage_content_is = graphene.String()
    firstmessage_content_id = graphene.String()
    firstmessage_content_ga = graphene.String()
    firstmessage_content_mk = graphene.String()
    firstmessage_content_mn = graphene.String()
    firstmessage_content_ne = graphene.String()
    firstmessage_content_ro = graphene.String()
    firstmessage_content_sr = graphene.String()
    firstmessage_content_sk = graphene.String()
    firstmessage_content_ta = graphene.String()
    firstmessage_content_tg = graphene.String()
    firstmessage_content_tr = graphene.String()
    firstmessage_content_ur = graphene.String()
    firstmessage_content_uz = graphene.String()


# single thread
class FirstMessageMsgsFilter(FilterSet):
    class Meta:
        model = FirstMessage
        fields = ("by_user_id", "content", "timestamp")
        order_by = ("-timestamp", "id")


class FirstMessageMsgsType(DjangoObjectType):
    class Meta:
        model = FirstMessage
        fields = "__all__"
        interfaces = (relay.Node,)

    def resolve_content(self, info):
        return getattr(self, translated_field_name(info.context.user, "content"))

    def resolve_timestamp(self, info):
        return info.context.user.date_joined + datetime.timedelta(milliseconds=100)
