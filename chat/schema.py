import re
import channels_graphql_ws
from chat.serializer import ChatQueueType
import graphene
from django.utils import timezone
from graphene_django.filter import DjangoFilterConnectionField

# from graphql_auth import mutations
# from graphql_auth.schema import MeQuery
# import graphql_jwt
from django.db.models import Q
from django.db.models import OuterRef, Count, Subquery
from django.db.models import Case, Value, When, F
from django.db.models import Value
from django.db import models
from django.db.models import Max
from django.db.models.functions import Coalesce, ExtractDay, ExtractHour

from graphene_django import DjangoObjectType
from django_filters import FilterSet, CharFilter
from datetime import datetime
from graphene import relay
from graphene.types.generic import GenericScalar
from chat.models import *
from chat.serializer import *
from user.models import CoinSettings, ChatsQue, CoinSettingsForRegion
from graphql.error import GraphQLError
from purchase.decorators import check_permission

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

from django.contrib.auth import get_user_model
from datetime import datetime
import datetime as datetime_parent

import googletrans
from googletrans import Translator

from .models import Message
from defaultPicker.utils import translated_field_name, custom_translate
from user.utils import translate_error_message
from user.models import UserForModsRestriction
translator = Translator()
lg = googletrans.LANGUAGES


User = get_user_model()


class NotificationSettingType(DjangoObjectType):
    class Meta:
        model = NotificationSettings
        fields = "__all__"

    def resolve_title(self, info):
        return getattr(self, translated_field_name(info.context.user, "title"))

    def resolve_message_str(self, info):
        return getattr(self, translated_field_name(info.context.user, "message_str"))


class NotificationFilter(FilterSet):
    pk = CharFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Notification
        fields = []

    @property
    def qs(self):
        # The query context can be found in self.request.
        qs = super(NotificationFilter, self).qs.filter(
            user=self.request.user, seen=False
        )
        # qs.update(seen=True)
        return qs.order_by("-created_date")


class TextType(graphene.ObjectType):
    title = graphene.String()
    body = graphene.String()


class NotificationType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    notification_data = graphene.Field(TextType)

    class Meta:
        model = Notification
        filterset_class = NotificationFilter
        fields = (
            "user",
            "priority",
            "created_date",
            "app_url",
            "sender",
            "seen",
            "notification_setting",
            "notification_body",
            "data",
        )
        interfaces = (relay.Node,)

    def resolve_notification_data(self, info):
        title = ""
        body = self.notification_body
        user = info.context.user

        if self.notification_setting:
            title = getattr(self.notification_setting,
                            translated_field_name(user, "title"))

        body = custom_translate(user, body)

        return TextType(title, body)


class HasMessageType(graphene.ObjectType):
    show_message_button = graphene.Boolean()


class FreeMessageLimitType(DjangoObjectType):
    class Meta:
        model = FreeMessageLimit
        fields = "__all__"
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    me = graphene.Field(ChatUserType)

    users = graphene.List(ChatUserType)
    user_search = graphene.List(
        ChatUserType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    user_name = graphene.List(ChatUserType, name=graphene.String())

    notes = graphene.List(NoteType, room_id=graphene.Int())
    # allnotes = graphene.List(NoteType)

    rooms = DjangoFilterConnectionField(RoomType, filterset_class=RoomFilter)
    room = graphene.Field(RoomType, id=graphene.ID())
    free_message_limit = graphene.Field(FreeMessageLimitType)

    messages = DjangoFilterConnectionField(
        MessageType,
        filterset_class=MessageFilter,
        id=graphene.ID(),
        first=graphene.Int(),
        skip=graphene.Int(),
        moderator_id=graphene.String(),
    )

    messages_for_workers = DjangoFilterConnectionField(
        MessageType,
        filterset_class=MessageFilter,
        id=graphene.ID(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    messages_statistics = graphene.List(
        MessageStatisticsType,
        worker_id=graphene.String(),
        month=graphene.Int(required=True),
    )
    same_day_messages_statistics = graphene.List(
        SameDayMessageStatisticsType, worker_id=graphene.String(required=True)
    )
    #
    broadcast = graphene.Field(BroadcastType)

    broadcast_msgs = DjangoFilterConnectionField(
        BroadcastMsgsType,
        filterset_class=BroadcastMsgsFilter,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    #
    firstmessage = graphene.Field(FirstMessageType)

    firstmessage_msgs = DjangoFilterConnectionField(
        FirstMessageMsgsType,
        filterset_class=FirstMessageMsgsFilter,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    moderators_in_queue = graphene.List(ModeratorQueueType)
    chats_in_queue = graphene.List(ChatQueueType)
    #
    notifications = DjangoFilterConnectionField(NotificationType)
    notification_settings = graphene.List(NotificationSettingType)
    unseen_count = graphene.Int()
    notification = graphene.Field(NotificationType, id=graphene.Int())

    has_message = graphene.Field(HasMessageType, target_id=graphene.String())
    last_seen_message_user = graphene.Field(
        MessageType, room_id=graphene.Int())

    def resolve_free_message_limit(self, info):
        obj = FreeMessageLimit.objects.first()
        user_id = User.objects.get(username="RealUser1")
        moderator_id = User.objects.get(username="Moderatior")
        if UserForModsRestriction.objects.filter(Q(user=user_id),
                                                 ~Q(moderators__id=moderator_id.id)
                                                 ).exists():
            print("user restricted")
        else:
            print("user NOT restricted")
        return obj

    def resolve_last_seen_message_user(self, info, room_id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        room = Room.objects.filter(id=room_id)
        if room.count() == 0:
            raise Exception(translate_error_message(
                info.context.user, "Room does not exist"))

        room = room.filter(Q(user_id=user) | Q(target=user))

        if room.count() == 0:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed in this Room"))
        else:
            room = room[0]

        try:
            message_seen = Message.objects.filter(
                room_id=room, read__isnull=False, user_id=user,
                restricted_msg=False
            ).first()
        except:
            raise Exception(translate_error_message(
                info.context.user, "Error whlie fetching  lastseen mesage  by receiver"))

        return message_seen

    def resolve_has_message(self, info, target_id=None):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in")
        messages_count = Message.objects.filter(
            restricted_msg=False,
            room_id_id__in=Subquery(
                Room.objects.filter(
                    user_id_id=info.context.user.id, target_id=target_id
                ).values("id")
            )
        ).count()
        hm = HasMessageType()
        hm.show_message_button = False if messages_count > 0 else True
        return hm

    def resolve_unseen_count(root, info):
        return Notification.objects.filter(user=info.context.user, seen=False).count()

    def resolve_notification(root, info, id):
        user = info.context.user

        if not user or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in"))

        try:
            notification = Notification.objects.get(id=id)
        except Notification.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "Notification does not exist"))

        if not notification.user_has_read_permission(user):
            raise Exception(translate_error_message(
                info.context.user, "Unauthorized access"))

        notification.set_seen()
        return notification

    def resolve_notification_settings(root, info):
        return NotificationSettings.objects.all()

    @staticmethod
    def resolve_moderators_in_queue(cls, info):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You are not logged in"))

        if not user.roles.filter(role__in=["ADMIN", "CHATTER"]):
            raise Exception(translate_error_message(
                info.context.user, "Unauthorized access"))

        return ModeratorQue.objects.all()

    @staticmethod
    def resolve_chats_in_queue(cls, info):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You are not logged in"))

        if not user.roles.filter(role__in=["ADMIN", "CHATTER"]):
            raise Exception(translate_error_message(
                info.context.user, "Unauthorized access"))
        return ChatsQue.objects.filter(
        room_id__in=Room.objects.all().values('id')
        )
    @staticmethod
    def resolve_messages_statistics(cls, info, worker_id=None, month=None, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))
        try:
            worker = User.objects.get(id=worker_id)
        except User.DoesNotExist:
            return Exception(translate_error_message(info.context.user, "Invalid worker_id"))
        # if user.roles.filter(role__in=['ADMIN']):
        #     try:
        #         worker=User.objects.get(id=worker_id)
        #     except User.DoesNotExist:
        #         return Exception("Invalid worker_id")
        # elif user.roles.filter(role__in=['CHATTER']):
        #     worker=user
        # else:
        #     raise Exception("You must be ADMIN or CHATTER to access this API")

        current_date = datetime.now()
        return (
            Message.objects.filter(
                Q(
                    timestamp__month=month,
                    timestamp__year=current_date.year,
                    sender_worker=worker,
                    restricted_msg=False,
                )
                | Q(
                    timestamp__month=month,
                    timestamp__year=current_date.year,
                    receiver_worker=worker,
                    restricted_msg=False,
                )
            )
            .annotate(
                day=ExtractDay("timestamp"),
            )
            .values("day")
            .annotate(sent_count=Count("sender_worker"))
            .annotate(received_count=Count("receiver_worker"))
            .order_by("day")
            .values(
                "day",
                "sent_count",
                "received_count",
                "room_id__user_id__id",
                "room_id__target__id",
            )
        )

    @staticmethod
    def resolve_same_day_messages_statistics(cls, info, worker_id=None, **kwargs):
        # user= user = info.context.user
        # if not (list(user.roles.all().values_list("role")) == [('REGULAR',), ('CHATTER',)]):
        #     return Exception("Invalid user")

        try:
            worker = User.objects.get(id=worker_id)
        except User.DoesNotExist:
            return Exception(translate_error_message(info.context.user, "Invalid worker_id"))

        current_date = datetime.now()
        # day = timezone.datetime.today().day
        return (
            Message.objects.filter(
                Q(
                    timestamp__day=current_date.day,
                    timestamp__month=current_date.month,
                    timestamp__year=current_date.year,
                    sender_worker=worker,
                    restricted_msg=False,
                )
            )
            .annotate(
                hour=ExtractHour("timestamp"),
            )
            .values("hour")
            .annotate(sent_count=Count("sender_worker"))
            .annotate(received_count=Count("receiver_worker"))
            .order_by("hour")
            .values("hour", "sent_count", "received_count")
        )

    @staticmethod
    def resolve_users(self, info):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        return get_user_model().objects.all()

    @staticmethod
    def resolve_user_search(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        qs = get_user_model().objects.all()

        if search:
            qs = qs.filter(username__icontains=search)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @staticmethod
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception(translate_error_message(
                info.context.user, "Not logged in!"))

        return user
    #list all user chat screen room / chats
    @staticmethod
    def resolve_rooms(cls, info, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        user_rooms = Room.objects.none()

        # unread all except sent by me;
        if user.fake_users.all().count() > 0:
            fake_users = user.fake_users.all()
            chatqueue = ChatsQue.objects.filter(worker=user, isAssigned=True)
            if chatqueue.count() > 0:
                room_id_in_chatque = chatqueue[0].room_id
                user_rooms = (
                    Room.objects.filter(
                        Q(user_id__in=fake_users) | Q(target__in=fake_users)
                    )
                    .exclude(
                        Q(user_id__in=fake_users, deleted=1)
                        | Q(target__in=fake_users, deleted=2)
                    )
                    .order_by("-last_modified")
                    .annotate(
                        blocked=Max(
                            Case(
                                When(
                                    Q(user_id=user)
                                    & Q(target__blockedUsers__username=user.username),
                                    then=2,
                                ),
                                When(
                                    Q(target=user)
                                    & Q(user_id__blockedUsers__username=user.username),
                                    then=2,
                                ),
                                When(
                                    Q(user_id=user)
                                    & Q(
                                        user_id__blockedUsers__username=F(
                                            "target__username"
                                        )
                                    ),
                                    then=1,
                                ),
                                When(
                                    Q(target=user)
                                    & Q(
                                        target__blockedUsers__username=F(
                                            "user_id__username"
                                        )
                                    ),
                                    then=1,
                                ),
                                default=Value(0),
                                output_field=models.IntegerField(),
                            )
                        ),
                        unread=Coalesce(
                            Subquery(
                                Message.objects.filter(
                                    room_id=OuterRef("pk"), read__isnull=True,
                                    restricted_msg=False,
                                )
                                .exclude(user_id__in=fake_users)
                                .values("room_id")
                                .annotate(count=Count("pk"))
                                .values("count"),
                                output_field=models.IntegerField(default=0),
                            ),
                            Value(0),
                        ),
                    )
                )
                user_rooms = user_rooms.filter(id=room_id_in_chatque)
        else:
            user_rooms = (
                Room.objects.filter(Q(user_id=user) | Q(target=user))
                .exclude(Q(user_id=user, deleted=1) | Q(target=user, deleted=2))
                .order_by("-last_modified")
                .annotate(
                    blocked=Max(
                        Case(
                            When(
                                Q(user_id=user)
                                & Q(target__blockedUsers__username=user.username),
                                then=2,
                            ),
                            When(
                                Q(target=user)
                                & Q(user_id__blockedUsers__username=user.username),
                                then=2,
                            ),
                            When(
                                Q(user_id=user)
                                & Q(
                                    user_id__blockedUsers__username=F(
                                        "target__username"
                                    )
                                ),
                                then=1,
                            ),
                            When(
                                Q(target=user)
                                & Q(
                                    target__blockedUsers__username=F(
                                        "user_id__username"
                                    )
                                ),
                                then=1,
                            ),
                            default=Value(0),
                            output_field=models.IntegerField(),
                        )
                    ),
                    unread=Coalesce(
                        Subquery(
                            Message.objects.filter(
                                room_id=OuterRef("pk"), read__isnull=True,
                                restricted_msg=False,
                            )
                            .exclude(user_id=user)
                            .values("room_id")
                            .annotate(count=Count("pk"))
                            .values("count"),
                            output_field=models.IntegerField(default=0),
                        ),
                        Value(0),
                    ),
                )
            )

        # user_rooms = (Room.objects.filter(Q(user_id=user) | Q(target=user)).order_by('-last_modified')
        #     .annotate(unread=Coalesce(Subquery(Message.objects.filter(room_id=OuterRef('pk'),read__isnull=True).exclude(user_id=user).values('room_id').annotate(count=Count('pk')).values('count'), output_field=models.IntegerField(default=0)),Value(0))))

        return user_rooms

    # ~ New
    @staticmethod
    def resolve_broadcast(cls, info, **kwargs):
        # added on top of rooms.
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        deleted_upto = (
            user.broadcast_deleted_upto
            if user.broadcast_deleted_upto is not None
            else 0
        )
        read_upto = (
            user.broadcast_read_upto if user.broadcast_read_upto is not None else 0
        )

        print("deleted_upto", deleted_upto)

        broadcast = (
            Broadcast.objects.filter(
                id__gt=deleted_upto).order_by("timestamp").last()
        )
        unread = Broadcast.objects.filter(id__gt=read_upto).count()

        return BroadcastType(
            unread=int(unread),
            broadcast_timestamp=info.context.user.date_joined
            + datetime_parent.timedelta(milliseconds=100),
            broadcast_content=getattr(
                broadcast, translated_field_name(info.context.user, "content")
            )
            if broadcast
            else "",
            broadcast_content_fr=broadcast.content_fr if broadcast else "",
            broadcast_content_zh_cn=broadcast.content_zh_cn if broadcast else "",
            broadcast_content_nl=broadcast.content_nl if broadcast else "",
            broadcast_content_de=broadcast.content_de if broadcast else "",
            broadcast_content_sw=broadcast.content_sw if broadcast else "",
            broadcast_content_it=broadcast.content_it if broadcast else "",
            broadcast_content_ar=broadcast.content_ar if broadcast else "",
            broadcast_content_iw=broadcast.content_iw if broadcast else "",
            broadcast_content_ja=broadcast.content_ja if broadcast else "",
            broadcast_content_ru=broadcast.content_ru if broadcast else "",
            broadcast_content_fa=broadcast.content_fa if broadcast else "",
            broadcast_content_pt_br=broadcast.content_pt_br if broadcast else "",
            broadcast_content_pt_pt=broadcast.content_pt_pt if broadcast else "",
            broadcast_content_es=broadcast.content_es if broadcast else "",
            broadcast_content_es_419=broadcast.content_es_419 if broadcast else "",
            broadcast_content_el=broadcast.content_el if broadcast else "",
            broadcast_content_zh_tw=broadcast.content_zh_tw if broadcast else "",
            broadcast_content_uk=broadcast.content_uk if broadcast else "",
            broadcast_content_ko=broadcast.content_ko if broadcast else "",
            broadcast_content_br=broadcast.content_br if broadcast else "",
            broadcast_content_pl=broadcast.content_pl if broadcast else "",
            broadcast_content_vi=broadcast.content_vi if broadcast else "",
            broadcast_content_nn=broadcast.content_nn if broadcast else "",
            broadcast_content_no=broadcast.content_no if broadcast else "",
            broadcast_content_sv=broadcast.content_sv if broadcast else "",
            broadcast_content_hr=broadcast.content_hr if broadcast else "",
            broadcast_content_cs=broadcast.content_cs if broadcast else "",
            broadcast_content_da=broadcast.content_da if broadcast else "",
            broadcast_content_tl=broadcast.content_tl if broadcast else "",
            broadcast_content_fi=broadcast.content_fi if broadcast else "",
            broadcast_content_sl=broadcast.content_sl if broadcast else "",
            broadcast_content_sq=broadcast.content_sq if broadcast else "",
            broadcast_content_am=broadcast.content_am if broadcast else "",
            broadcast_content_hy=broadcast.content_hy if broadcast else "",
            broadcast_content_la=broadcast.content_la if broadcast else "",
            broadcast_content_lv=broadcast.content_lv if broadcast else "",
            broadcast_content_th=broadcast.content_th if broadcast else "",
            broadcast_content_az=broadcast.content_az if broadcast else "",
            broadcast_content_eu=broadcast.content_eu if broadcast else "",
            broadcast_content_be=broadcast.content_be if broadcast else "",
            broadcast_content_bn=broadcast.content_bn if broadcast else "",
            broadcast_content_bs=broadcast.content_bs if broadcast else "",
            broadcast_content_bg=broadcast.content_bg if broadcast else "",
            broadcast_content_km=broadcast.content_km if broadcast else "",
            broadcast_content_ca=broadcast.content_ca if broadcast else "",
            broadcast_content_et=broadcast.content_et if broadcast else "",
            broadcast_content_gl=broadcast.content_gl if broadcast else "",
            broadcast_content_ka=broadcast.content_ka if broadcast else "",
            broadcast_content_hi=broadcast.content_hi if broadcast else "",
            broadcast_content_hu=broadcast.content_hu if broadcast else "",
            broadcast_content_is=broadcast.content_is if broadcast else "",
            broadcast_content_id=broadcast.content_id if broadcast else "",
            broadcast_content_ga=broadcast.content_ga if broadcast else "",
            broadcast_content_mk=broadcast.content_mk if broadcast else "",
            broadcast_content_mn=broadcast.content_mn if broadcast else "",
            broadcast_content_ne=broadcast.content_ne if broadcast else "",
            broadcast_content_ro=broadcast.content_ro if broadcast else "",
            broadcast_content_sr=broadcast.content_sr if broadcast else "",
            broadcast_content_sk=broadcast.content_sk if broadcast else "",
            broadcast_content_ta=broadcast.content_ta if broadcast else "",
            broadcast_content_tg=broadcast.content_tg if broadcast else "",
            broadcast_content_tr=broadcast.content_tr if broadcast else "",
            broadcast_content_ur=broadcast.content_ur if broadcast else "",
            broadcast_content_uz=broadcast.content_uz if broadcast else "",
        )

    @staticmethod
    def resolve_broadcast_msgs(cls, info, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        deleted_upto = (
            user.broadcast_deleted_upto
            if user.broadcast_deleted_upto is not None
            else 0
        )

        user.broadcast_read_upto = Broadcast.objects.last().id
        user.save()

        broadcast = Broadcast.objects.filter(
            id__gt=deleted_upto).order_by("-timestamp")
        return broadcast

    # ~ New
    @staticmethod
    def resolve_firstmessage(cls, info, **kwargs):
        # added on top of rooms.
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        read_upto = (
            user.firstmessage_read_upto
            if user.firstmessage_read_upto is not None
            else 0
        )

        firstmessage = FirstMessage.objects.last()
        unread = FirstMessage.objects.filter(id__gt=read_upto).count()

        return FirstMessageType(
            unread=int(unread),
            firstmessage_timestamp=info.context.user.date_joined
            + datetime_parent.timedelta(milliseconds=100),
            firstmessage_content=getattr(
                firstmessage, translated_field_name(
                    info.context.user, "content")
            )
            if firstmessage
            else "",
            firstmessage_content_fr=firstmessage.content_fr if firstmessage else "",
            firstmessage_content_zh_cn=firstmessage.content_zh_cn
            if firstmessage
            else "",
            firstmessage_content_nl=firstmessage.content_nl if firstmessage else "",
            firstmessage_content_de=firstmessage.content_de if firstmessage else "",
            firstmessage_content_sw=firstmessage.content_sw if firstmessage else "",
            firstmessage_content_it=firstmessage.content_it if firstmessage else "",
            firstmessage_content_ar=firstmessage.content_ar if firstmessage else "",
            firstmessage_content_iw=firstmessage.content_iw if firstmessage else "",
            firstmessage_content_ja=firstmessage.content_ja if firstmessage else "",
            firstmessage_content_ru=firstmessage.content_ru if firstmessage else "",
            firstmessage_content_fa=firstmessage.content_fa if firstmessage else "",
            firstmessage_content_pt_br=firstmessage.content_pt_br
            if firstmessage
            else "",
            firstmessage_content_pt_pt=firstmessage.content_pt_pt
            if firstmessage
            else "",
            firstmessage_content_es=firstmessage.content_es if firstmessage else "",
            firstmessage_content_es_419=firstmessage.content_es_419
            if firstmessage
            else "",
            firstmessage_content_el=firstmessage.content_el if firstmessage else "",
            firstmessage_content_zh_tw=firstmessage.content_zh_tw
            if firstmessage
            else "",
            firstmessage_content_uk=firstmessage.content_uk if firstmessage else "",
            firstmessage_content_ko=firstmessage.content_ko if firstmessage else "",
            firstmessage_content_br=firstmessage.content_br if firstmessage else "",
            firstmessage_content_pl=firstmessage.content_pl if firstmessage else "",
            firstmessage_content_vi=firstmessage.content_vi if firstmessage else "",
            firstmessage_content_nn=firstmessage.content_nn if firstmessage else "",
            firstmessage_content_no=firstmessage.content_no if firstmessage else "",
            firstmessage_content_sv=firstmessage.content_sv if firstmessage else "",
            firstmessage_content_hr=firstmessage.content_hr if firstmessage else "",
            firstmessage_content_cs=firstmessage.content_cs if firstmessage else "",
            firstmessage_content_da=firstmessage.content_da if firstmessage else "",
            firstmessage_content_tl=firstmessage.content_tl if firstmessage else "",
            firstmessage_content_fi=firstmessage.content_fi if firstmessage else "",
            firstmessage_content_sl=firstmessage.content_sl if firstmessage else "",
            firstmessage_content_sq=firstmessage.content_sq if firstmessage else "",
            firstmessage_content_am=firstmessage.content_am if firstmessage else "",
            firstmessage_content_hy=firstmessage.content_hy if firstmessage else "",
            firstmessage_content_la=firstmessage.content_la if firstmessage else "",
            firstmessage_content_lv=firstmessage.content_lv if firstmessage else "",
            firstmessage_content_th=firstmessage.content_th if firstmessage else "",
            firstmessage_content_az=firstmessage.content_az if firstmessage else "",
            firstmessage_content_eu=firstmessage.content_eu if firstmessage else "",
            firstmessage_content_be=firstmessage.content_be if firstmessage else "",
            firstmessage_content_bn=firstmessage.content_bn if firstmessage else "",
            firstmessage_content_bs=firstmessage.content_bs if firstmessage else "",
            firstmessage_content_bg=firstmessage.content_bg if firstmessage else "",
            firstmessage_content_km=firstmessage.content_km if firstmessage else "",
            firstmessage_content_ca=firstmessage.content_ca if firstmessage else "",
            firstmessage_content_et=firstmessage.content_et if firstmessage else "",
            firstmessage_content_gl=firstmessage.content_gl if firstmessage else "",
            firstmessage_content_hi=firstmessage.content_hi if firstmessage else "",
            firstmessage_content_hu=firstmessage.content_hu if firstmessage else "",
            firstmessage_content_is=firstmessage.content_is if firstmessage else "",
            firstmessage_content_id=firstmessage.content_id if firstmessage else "",
            firstmessage_content_ga=firstmessage.content_ga if firstmessage else "",
            firstmessage_content_mk=firstmessage.content_mk if firstmessage else "",
            firstmessage_content_mn=firstmessage.content_mn if firstmessage else "",
            firstmessage_content_ne=firstmessage.content_ne if firstmessage else "",
            firstmessage_content_ro=firstmessage.content_ro if firstmessage else "",
            firstmessage_content_sr=firstmessage.content_sr if firstmessage else "",
            firstmessage_content_sk=firstmessage.content_sk if firstmessage else "",
            firstmessage_content_ta=firstmessage.content_ta if firstmessage else "",
            firstmessage_content_tg=firstmessage.content_tg if firstmessage else "",
            firstmessage_content_tr=firstmessage.content_tr if firstmessage else "",
            firstmessage_content_ur=firstmessage.content_ur if firstmessage else "",
            firstmessage_content_uz=firstmessage.content_uz if firstmessage else "",
        )

    @staticmethod
    def resolve_firstmessage_msgs(cls, info, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        user.firstmessage_read_upto = FirstMessage.objects.last().id
        user.save()
        return FirstMessage.objects.all().order_by("-timestamp")

    @staticmethod
    def resolve_notes(cls, info, room_id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))
        roles = [r.role for r in user.roles.all()]
        if "REGULAR" not in roles and "CHATTER" not in roles:
            raise Exception(translate_error_message(
                info.context.user, "The user is not worker"))

        fake_users = user.fake_users.all()
        if room := Room.objects.filter(
            Q(id=room_id, user_id__in=fake_users) | Q(
                id=room_id, target__in=fake_users)
        ).exclude(
            Q(id=room_id, user_id__in=fake_users, deleted=1)
            | Q(id=room_id, target__in=fake_users, deleted=2)
        ):
            room = room[0]
        else:
            raise Exception(translate_error_message(
                info.context.user, "Room not found"))

        return Notes.objects.filter(room_id=room_id)

    @staticmethod
    def resolve_room(cls, info, id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        return Room.objects.get(id=id)

    @staticmethod
    def resolve_user_name(cls, info, name, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "Not logged in!"))
        # query = "Select * from User where fullName like '%{}%'".format(name)
        # print("query here ")
        # print(query)
        # return User.objects.raw(query)
        return User.objects.filter(fullName__icontains=name)

    # result = table.objects.filter(string__contains='pattern')

    @staticmethod
    def resolve_messages(
        cls, info, id, skip=None, last=None, moderator_id=None, **kwargs
    ):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        if (
            moderator_id
        ):  # if message sent my moderator then set user to moderator user.
            if not user.fake_users.filter(id=moderator_id).exists():
                raise Exception(translate_error_message(
                    info.context.user, "Invalid moderator id"))
            user = User.objects.get(id=moderator_id)

        room = Room.objects.get(id=id)
        if user not in [room.user_id, room.target]:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed to view this chat"))

        if user == room.user_id:
            user_for_notification = room.target

        if user == room.target:
            user_for_notification = room.user_id

        user.see_unseen_message_reminders()

        # read all except sent by me;
        Message.objects.filter(room_id=room, read__isnull=True, restricted_msg=False).exclude(
            user_id=user
        ).update(read=datetime.now())

        notifications = Notification.objects.filter(
            notification_setting__id="SNDMSG", user=user, seen=False
        )
        for notification in notifications:
            if notification.data:
                try:
                    room_id = re.findall(
                        r"roomID\':\s(\d+?),", notification.data)
                    if room_id:
                        print(f"room.id: {room.id}")
                        print(
                            f"Notifications found: Sent room.id: {room.id} | room_id:{room_id[0]} by {user.email}"
                        )

                        room__id_int = int(room_id[0])
                        if room__id_int == room.id:
                            notification.seen = True
                            notification.save()
                            print(
                                f"Notifications found: Sent room.id: {room.id} | room_id:{room__id_int} by {user.email}"
                            )

                except Exception as e:
                    raise Exception(
                        translate_error_message(
                            info.context.user, f"Exception Notififcation Data: {notification.data} - {e}")
                    )

        # return Message.objects.filter(room_id=room).order_by('timestamp')
        qs = Message.objects.filter(room_id=room, is_deleted=False,
                                    restricted_msg=False).order_by(
            "-timestamp"
        )
        try:
            message_seen = (
                Message.objects.filter(room_id=id, read__isnull=False,
                                       restricted_msg=False)
                .exclude(user_id=user)
                .first()
            )
            if message_seen is not None:
                OnSeenMessageByReceiver.broadcast(
                    payload=message_seen, group=str(user_for_notification.id)
                )

        except:
            raise Exception(translate_error_message(
                info.context.user, "Error whlie broadcasting lastseen mesage  by receiver"))
        if skip:
            qs = qs[skip:]

        if last:
            qs = qs[:last]

        return qs

    @staticmethod
    def resolve_messages_for_workers(
        cls, info, id, skip=None, last=None, **kwargs
    ):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        room = Room.objects.get(id=id)

        # read all except sent by me;
        Message.objects.filter(room_id=room, read__isnull=True, restricted_msg=False).exclude(
            user_id=user
        ).update(read=datetime.now())

        notifications = Notification.objects.filter(
            notification_setting__id="SNDMSG", user=user, seen=False
        )
        for notification in notifications:
            if notification.data:
                try:
                    room_id = re.findall(
                        r"roomID\':\s(\d+?),", notification.data)
                    if room_id:
                        print(f"room.id: {room.id}")
                        print(
                            f"Notifications found: Sent room.id: {room.id} | room_id:{room_id[0]} by {user.email}"
                        )

                        room__id_int = int(room_id[0])
                        if room__id_int == room.id:
                            notification.seen = True
                            notification.save()
                            print(
                                f"Notifications found: Sent room.id: {room.id} | room_id:{room__id_int} by {user.email}"
                            )

                except Exception as e:
                    raise Exception(
                        translate_error_message(
                            info.context.user, f"Exception Notififcation Data: {notification.data} - {e}")
                    )

        # return Message.objects.filter(room_id=room).order_by('timestamp')
        qs = Message.objects.filter(room_id=room, is_deleted=False,
                                    restricted_msg=False).order_by(
            "-timestamp"
        )
        if skip:
            qs = qs[skip:]

        if last:
            qs = qs[:last]

        return qs


class CreateChat(graphene.Mutation):
    """
    to creeate a chat you need to pass `user_name`
    """

    room = graphene.Field(RoomType)
    error = graphene.String()

    class Arguments:
        user_name = graphene.String(required=True)
        moderator_id = graphene.String(required=False)

    @classmethod
    def mutate(cls, _, info, user_name=None, moderator_id=None):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        try:
            target_user = User.objects.prefetch_related("blockedUsers").get(
                username=user_name
            )
        except User.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "User name not found"))

        # if user.id != moderator_id:
        #     raise Exception("User is not moderator.")

        if user.fake_users.all().count() > 0:
            if not moderator_id:
                raise Exception(translate_error_message(
                    info.context.user, "moderator_id required"))

            if not user.fake_users.filter(id=moderator_id).exists():
                raise Exception(translate_error_message(
                    info.context.user, "Invalid moderator id"))

            user = User.objects.get(id=moderator_id)

            if target_user.roles.filter(role="MODERATOR").exists():
                raise Exception(translate_error_message(
                    info.context.user, "Can not chat Moderator with Moderator"))

        if user.username == user_name:
            raise Exception(translate_error_message(
                info.context.user, "You can not chat with yourself."))

        # If either user or target_user blocked other than Room can't be created
        if target_user.has_blocked(user):
            raise Exception(translate_error_message(
                info.context.user, "This User no longer accepts PMs."))

        if user.has_blocked(target_user):
            raise Exception(translate_error_message(
                info.context.user, "Unblock this user to send a new message"))

        room_name_a = [user.username, user_name]
        room_name_a.sort()
        room_name_str = f"{room_name_a[0]}_{room_name_a[1]}"

        try:
            chat_room = Room.objects.get(name=room_name_str)
        except Room.DoesNotExist:
            chat_room = Room(
                name=room_name_str,
                user_id=User.objects.get(id=user.id),
                target=target_user,
            )
            chat_room.save()

        return CreateChat(room=chat_room)


class CreateChatAllModerator(graphene.Mutation):
    """
    to creeate a chat you need to pass `user_name`
    """

    room = graphene.Field(RoomType)
    error = graphene.String()

    class Arguments:
        user_name = graphene.String(required=True)
        moderator_id = graphene.String(required=False)

    @classmethod
    def mutate(cls, _, info, user_name=None, moderator_id=None):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        try:
            target_user = User.objects.prefetch_related("blockedUsers").get(
                username=user_name
            )
        except User.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "User name not found"))

        # if user.id != moderator_id:
        #     raise Exception("User is not moderator.")

        if not moderator_id:
            raise Exception(translate_error_message(
                info.context.user, "moderator_id required"))

        if not User.objects.filter(Q(id=moderator_id),
                                   Q(roles__role__in=["MODERATOR"]) |
                                   Q(email__endswith="i69app.com")
                                   ).exists():
            raise Exception(translate_error_message(
                info.context.user, "Invalid moderator id"))

        user = User.objects.get(id=moderator_id)

        if target_user.roles.filter(role="MODERATOR").exists():
            raise Exception(translate_error_message(
                info.context.user, "Can not chat Moderator with Moderator"))

        if user.username == user_name:
            raise Exception(translate_error_message(
                info.context.user, "You can not chat with yourself."))

        # If either user or target_user blocked other than Room can't be created
        if target_user.has_blocked(user):
            raise Exception(translate_error_message(
                info.context.user, "This User no longer accepts PMs."))

        if user.has_blocked(target_user):
            raise Exception(translate_error_message(
                info.context.user, "Unblock this user to send a new message"))

        room_name_a = [user.username, user_name]
        room_name_a.sort()
        room_name_str = f"{room_name_a[0]}_{room_name_a[1]}"

        try:
            chat_room = Room.objects.get(name=room_name_str)
        except Room.DoesNotExist:
            chat_room = Room(
                name=room_name_str,
                user_id=User.objects.get(id=user.id),
                target=target_user,
            )
            chat_room.save()

        return CreateChatAllModerator(room=chat_room)


class CreateNotes(graphene.Mutation):
    """
    to creeate notes you need to pass `room id and content`
    """

    notes = graphene.Field(NoteType)
    error = graphene.String()

    class Arguments:
        room_id = graphene.Int(required=True)
        content = graphene.String(required=True)
        forRealUser = graphene.Boolean(required=True)

    @classmethod
    def mutate(cls, _, info, room_id=None, content=None, forRealUser=None):

        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        roles = [r.role for r in user.roles.all()]
        if "REGULAR" not in roles and "CHATTER" not in roles:
            raise Exception(translate_error_message(
                info.context.user, "The user is not worker"))

        fake_users = user.fake_users.all()
        room = Room.objects.filter(
            Q(id=room_id, user_id__in=fake_users) | Q(
                id=room_id, target__in=fake_users)
        ).exclude(
            Q(id=room_id, user_id__in=fake_users, deleted=1)
            | Q(id=room_id, target__in=fake_users, deleted=2)
        )
        if room:
            room = room[0]
        else:
            raise Exception(translate_error_message(
                info.context.user, "Room not found"))

        notes = Notes.objects.get_or_create(
            room_id=room, forRealUser=forRealUser)
        notes[0].content = content
        notes[0].save()
        return CreateNotes(notes=notes[0])


class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)
    # message = graphene.String()

    class Arguments:
        message_str = graphene.String(required=True)
        room_id = graphene.Int(required=True)
        moderator_id = graphene.String()
        message_str_type = graphene.String()

    @classmethod
    def mutate(
        cls, _, info, message_str, room_id, moderator_id=None, message_str_type="C"
    ):
        if len(message_str_type.strip()) < 1:
            message_str_type = "C"
        if message_str_type == "GL":
            coin_method = "SHARE_LOCATION"
        else:
            coin_method = "Message"

        message_type_exists = [
            True for x in Message.MESSAGE_TYPES if message_str_type in x[0]
        ]
        if not message_type_exists:
            raise Exception(translate_error_message(
                info.context.user, "Invalid message type"))
        user = info.context.user
        roles = [r.role for r in user.roles.all()]
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        room = Room.objects.get(pk=room_id)
        worker = None
        if (
            moderator_id
        ):  # if message sent my moderator then set user to moderator user.
            if not user.fake_users.filter(id=moderator_id).exists():
                raise Exception(translate_error_message(
                    info.context.user, "Invalid moderator id"))
            worker = user
            user = User.objects.get(id=moderator_id)

        if user != room.user_id and user != room.target:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed to post or view this chat"))

        sender_user = room.user_id if room.user_id == user else room.target
        if user == room.user_id:
            user_for_notification = room.target

        if user == room.target:
            user_for_notification = room.user_id

        if user_for_notification.has_blocked(user):
            raise Exception(translate_error_message(
                info.context.user, "This user no longer accept PM'S."))

        if user.has_blocked(user_for_notification):
            raise Exception(translate_error_message(
                info.context.user, "Unblock this user before to send him a new message"))

        if room.deleted > 0:
            room.deleted = 0
            room.save()
        if "REGULAR" not in roles and "CHATTER" not in roles:
            messages = Message.objects.filter(room_id_id=room.id)
            current_date = datetime.now()
            message_qs = Message.objects.filter(user_id=user)
            # users_count = len(message_qs.filter(
            #     timestamp__day=current_date.day,
            #     timestamp__month=current_date.month,
            #     timestamp__year=current_date.year,
            # ).values('room_id__target__email').annotate(
            #     count=Count("room_id__target")
            # ).order_by('room_id__target').distinct())

            # free_message_limit = FreeMessageLimit.objects.first().user

            has_permision = check_permission(
                user=user,
                permission="FIRST_FREE_MESSAGE",
                date_field="timestamp",
                qs=message_qs,
                room=room,
            )

            if not has_permision:
                coins = CoinSettings.objects.filter(method=coin_method).first()
                coins_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coins, region=user.get_coinsettings_region()
                )
                if coins_for_region.count():
                    coins = coins_for_region.first()

                if coins and coins.coins_needed > 0:
                    user.deductCoins(coins.coins_needed, coin_method)
                    user.save()
                else:
                    raise Exception(
                        translate_error_message(info.context.user, "Insufficient coins: {} coins required".format(
                            coins.coins_needed)
                        )
                    )
        if message_str_type == "G":
            message = Message(
                room_id=room,
                user_id=user,
                content=message_str,
                message_type=message_str_type,
                gift_message_sender=user
            )
        else:
            message = Message(
                room_id=room,
                user_id=user,
                content=message_str,
                message_type=message_str_type,
            )

        if user.roles.filter(role="MODERATOR"):
            message.sender_worker = worker
            chatque = ChatsQue.objects.filter(room_id=room.id)
            worker.user_last_seen = timezone.now()
            worker.save()

            last_message = (
                Message.objects.filter(
                    room_id=room, message_type=message_str_type)
                .order_by("-timestamp")
                .first()
            )

            # Update the receiver_worker only if the message is not sent by the Moderator
            if last_message and not last_message.sender_worker:
                if last_message.receiver_worker:
                    last_message.receiver_worker = worker
                last_message.save()
            # print('chat que is ',chatque)
            if chatque.count() > 0:
                print("=====chat queue deleted=======", chatque)
                chatque[0].moderator.owned_by.remove(worker)
                chatque[0].delete()

        elif room.target.roles.filter(role="MODERATOR") or room.user_id.roles.filter(
            role="MODERATOR"
        ):

            if room.target.roles.filter(role="MODERATOR"):
                if UserForModsRestriction.objects.filter(Q(user=room.user_id),
                                                         ~Q(moderators__id=room.target.id)
                                                         ).exists():
                    message.restricted_msg = True
                else:
                    ChatsQue.objects.get_or_create(
                        room_id=room.id, moderator=room.target)
            if message.restricted_msg is False:
                if room.user_id.roles.filter(role="MODERATOR"):
                    ChatsQue.objects.get_or_create(
                        room_id=room.id, moderator=room.user_id)

                if room.user_id == user:
                    if room.target.owned_by.all().count() > 0:
                        message.receiver_worker = room.target.owned_by.all()[0]

                else:
                    if room.user_id.owned_by.all().count() > 0:
                        message.receiver_worker = room.user_id.owned_by.all()[
                            0]

                chat = ChatsQue.objects.filter(
                    isAssigned=True, room_id=room.id).first()
                if chat:
                    message.receiver_worker = chat.worker

        message.save()

        room.last_modified = datetime.now()
        room.save()

        # user last online
        user.last_login = datetime.now()
        user.save()
        # if room.user_id == user:
        #     OnNewMessage.broadcast(payload=message, group=room.target.username)
        # else:
        #     OnNewMessage.broadcast(payload=message, group=room.user_id.username)
        #
        #     data = {
        #         "roomIDs": room_id,
        #         "notification_type": "chat_notification",
        #         "message": message_str,
        #         "user_avatar": "test url",
        #     }
        # SendNotification( user_id=moderator_id, data=data)
        if message.restricted_msg is False:
            notification_setting = "SNDMSG"
            app_url = None
            priority = None
            icon = None
            avatar_url = None
            # checks for avatar_url if None
            try:
                avatar_url = user.avatar().file.url
            except:
                avatar_url = None
            data = {
                "roomID": room.id,
                "notification_type": notification_setting,
                "message": message.content,
                "user_avatar": avatar_url,
                "title": "Sent message",
            }
            if avatar_url:
                icon = info.context.build_absolute_uri(avatar_url)
            android_channel_id = None
            notification_obj = Notification(
                user=user_for_notification,
                sender=user,
                app_url=app_url,
                notification_setting_id=notification_setting,
                data=data,
                priority=priority,
            )
            send_notification_fcm(
                notification_obj=notification_obj,
                android_channel_id=android_channel_id,
                icon=icon,
                image=icon,
            )

            # Send new message event to only receiver
            # OnNewMessage.broadcast(payload=message, group=str(user_for_notification.id))

            # Send create messae event to both sender and receiver
            OnNewMessage.broadcast(payload=message, group=str(room_id))
        # OnSeenMessageByReceiver.broadcast(payload=message, group=str(sender_user.id))
        # OnNewMessage.broadcast(payload=message, group=str(room.target.id))

        return SendMessage(message=message)


class SendMessageAllModerator(graphene.Mutation):
    message = graphene.Field(MessageType)
    # message = graphene.String()

    class Arguments:
        message_str = graphene.String(required=True)
        room_id = graphene.Int(required=True)
        moderator_id = graphene.String()
        message_str_type = graphene.String()

    @classmethod
    def mutate(
        cls, _, info, message_str, room_id, moderator_id=None, message_str_type="C"
    ):
        if len(message_str_type.strip()) < 1:
            message_str_type = "C"
        if message_str_type == "GL":
            coin_method = "SHARE_LOCATION"
        else:
            coin_method = "Message"

        message_type_exists = [
            True for x in Message.MESSAGE_TYPES if message_str_type in x[0]
        ]
        if not message_type_exists:
            raise Exception(translate_error_message(
                info.context.user, "Invalid message type"))
        user = info.context.user
        roles = [r.role for r in user.roles.all()]
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        room = Room.objects.get(pk=room_id)
        worker = None
        if (
            moderator_id
        ):  # if message sent my moderator then set user to moderator user.
            if not User.objects.filter(Q(id=moderator_id),
                                       Q(roles__role__in=["MODERATOR"]) |
                                       Q(email__endswith="i69app.com")
                                       ).exists():
                raise Exception(translate_error_message(
                    info.context.user, "Invalid moderator id"))
            worker = user
            user = User.objects.get(id=moderator_id)

        if user != room.user_id and user != room.target:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed to post or view this chat"))

        sender_user = room.user_id if room.user_id == user else room.target
        if user == room.user_id:
            user_for_notification = room.target

        if user == room.target:
            user_for_notification = room.user_id

        if user_for_notification.has_blocked(user):
            raise Exception(translate_error_message(
                info.context.user, "This user no longer accept PM'S."))

        if user.has_blocked(user_for_notification):
            raise Exception(translate_error_message(
                info.context.user, "Unblock this user before to send him a new message"))

        if room.deleted > 0:
            room.deleted = 0
            room.save()
        if "REGULAR" not in roles and "CHATTER" not in roles:
            messages = Message.objects.filter(room_id_id=room.id)
            current_date = datetime.now()
            message_qs = Message.objects.filter(user_id=user)
            # users_count = len(message_qs.filter(
            #     timestamp__day=current_date.day,
            #     timestamp__month=current_date.month,
            #     timestamp__year=current_date.year,
            # ).values('room_id__target__email').annotate(
            #     count=Count("room_id__target")
            # ).order_by('room_id__target').distinct())

            # free_message_limit = FreeMessageLimit.objects.first().user

            has_permision = check_permission(
                user=user,
                permission="FIRST_FREE_MESSAGE",
                date_field="timestamp",
                qs=message_qs,
                room=room,
            )

            if not has_permision:
                coins = CoinSettings.objects.filter(method=coin_method).first()
                coins_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coins, region=user.get_coinsettings_region()
                )
                if coins_for_region.count():
                    coins = coins_for_region.first()

                if coins and coins.coins_needed > 0:
                    user.deductCoins(coins.coins_needed, coin_method)
                    user.save()
                else:
                    raise Exception(
                        translate_error_message(info.context.user, "Insufficient coins: {} coins required".format(
                            coins.coins_needed)
                        )
                    )
        if message_str_type == "G":
            message = Message(
                room_id=room,
                user_id=user,
                content=message_str,
                message_type=message_str_type,
                gift_message_sender=user
            )
        else:
            message = Message(
                room_id=room,
                user_id=user,
                content=message_str,
                message_type=message_str_type,
            )

        if user.roles.filter(role="MODERATOR"):
            message.sender_worker = worker
            chatque = ChatsQue.objects.filter(room_id=room.id)
            worker.user_last_seen = timezone.now()
            worker.save()

            last_message = (
                Message.objects.filter(
                    room_id=room, message_type=message_str_type)
                .order_by("-timestamp")
                .first()
            )
            # Update the receiver_worker only if the message is not sent by the Moderator/worker
            if last_message and not last_message.sender_worker:
                if last_message.receiver_worker:
                    last_message.receiver_worker = worker
                last_message.save()
            # print('chat que is ',chatque)
            if chatque.count() > 0:
                print("=====chat queue deleted=======", chatque)
                chatque[0].moderator.owned_by.remove(worker)
                chatque[0].delete()

        elif room.target.roles.filter(role="MODERATOR") or room.user_id.roles.filter(
            role="MODERATOR"
        ):

            if room.target.roles.filter(role="MODERATOR"):
                if UserForModsRestriction.objects.filter(user=room.user_id).exists():
                    message.restricted_msg = True
                else:
                    ChatsQue.objects.get_or_create(
                        room_id=room.id, moderator=room.target)

            if room.user_id.roles.filter(role="MODERATOR"):
                ChatsQue.objects.get_or_create(
                    room_id=room.id, moderator=room.user_id)

            if room.user_id == user:
                if room.target.owned_by.all().count() > 0:
                    message.receiver_worker = room.target.owned_by.all()[0]

            else:
                if room.user_id.owned_by.all().count() > 0:
                    message.receiver_worker = room.user_id.owned_by.all()[0]

            chat = ChatsQue.objects.filter(
                isAssigned=True, room_id=room.id).first()
            if chat:
                message.receiver_worker = chat.worker

        message.save()

        room.last_modified = datetime.now()
        room.save()

        # user last online
        user.last_login = datetime.now()
        user.save()
        # if room.user_id == user:
        #     OnNewMessage.broadcast(payload=message, group=room.target.username)
        # else:
        #     OnNewMessage.broadcast(payload=message, group=room.user_id.username)
        #
        #     data = {
        #         "roomIDs": room_id,
        #         "notification_type": "chat_notification",
        #         "message": message_str,
        #         "user_avatar": "test url",
        #     }
        # SendNotification( user_id=moderator_id, data=data)
        notification_setting = "SNDMSG"
        app_url = None
        priority = None
        icon = None
        avatar_url = None
        # checks for avatar_url if None
        try:
            avatar_url = user.avatar().file.url
        except:
            avatar_url = None
        data = {
            "roomID": room.id,
            "notification_type": notification_setting,
            "message": message.content,
            "user_avatar": avatar_url,
            "title": "Sent message",
        }
        if avatar_url:
            icon = info.context.build_absolute_uri(avatar_url)
        android_channel_id = None
        notification_obj = Notification(
            user=user_for_notification,
            sender=user,
            app_url=app_url,
            notification_setting_id=notification_setting,
            data=data,
            priority=priority,
        )
        send_notification_fcm(
            notification_obj=notification_obj,
            android_channel_id=android_channel_id,
            icon=icon,
            image=icon,
        )

        # Send new message event to only receiver
        # OnNewMessage.broadcast(payload=message, group=str(user_for_notification.id))

        # Send create messae event to both sender and receiver
        OnNewMessage.broadcast(payload=message, group=str(room_id))
        # OnSeenMessageByReceiver.broadcast(payload=message, group=str(sender_user.id))
        # OnNewMessage.broadcast(payload=message, group=str(room.target.id))

        return SendMessageAllModerator(message=message)


class OnNewMessage(channels_graphql_ws.Subscription):
    message = graphene.Field(MessageType)
    notification_queue_limit = 64

    class Arguments:
        room_id = graphene.Int(required=True)
        token = graphene.String()
        moderator_id = graphene.String()

    def subscribe(self, info, token, room_id, moderator_id=None):
        # user = info.context.user

        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login = datetime.now()
            user.save()
            if user.fake_users.all().count() > 0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception(translate_error_message(
                            info.context.user, "Invalid moderator_id"))
                    user = User.objects.get(id=moderator_id)
                    user.last_login = datetime.now()
                    user.save()
                # else:
                #     raise Exception("moderator_id required")

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return [str(room_id)]

    def publish(self, info, token=None, room_id=None, moderator_id=None):
        message = Message.objects.get(id=self.id)
        return OnNewMessage(message=message)


class OnDeleteMessage(channels_graphql_ws.Subscription):
    id = graphene.Int()
    notification_queue_limit = 64

    class Arguments:
        room_id = graphene.Int(required=True)
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, room_id, token, moderator_id=None):
        # user = info.context.user
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login = datetime.now()
            user.save()
            if user.fake_users.all().count() > 0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception(translate_error_message(
                            info.context.user, "Invalid moderator_id"))
                    user = User.objects.get(id=moderator_id)
                    user.last_login = datetime.now()
                    user.save()
                else:
                    raise Exception(translate_error_message(
                        info.context.user, "moderator_id required"))
        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()
        # user = get_token_user(token=token,moderator_id=moderator_id)
        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return [str(room_id)]

    @staticmethod
    def publish(payload, info, room_id=None, token=None, moderator_id=None):
        return OnDeleteMessage(id=payload)


class SendNotification(graphene.Mutation):
    class Arguments:
        notification_setting = graphene.String()
        icon = graphene.String(required=False)

        user_id = graphene.UUID(required=True)
        app_url = graphene.String()
        priority = graphene.Int()
        data = GenericScalar()
        android_channel_id = graphene.String()

    sent = graphene.Boolean()

    def mutate(
        root,
        info,
        notification_setting,
        user_id,
        icon=None,
        app_url=None,
        priority=None,
        data=None,
        android_channel_id=None,
    ):

        user = User.objects.filter(id=user_id).first()
        if not user:
            raise Exception(translate_error_message(
                info.context.user, "User with this ID does not exist."))
        print("this is the payload ......")
        data = {}
        print(data)
        notification_obj = Notification(
            user=user,
            sender=info.context.user,
            app_url=app_url,
            notification_setting_id=notification_setting,
            data=data,
            priority=priority,
        )
        print("notification_obj")
        print(notification_obj)
        send_notification_fcm(
            notification_obj=notification_obj,
            android_channel_id=android_channel_id,
            icon=icon,
        )
        return SendNotification(sent=True)


class DeleteBroadcast(graphene.Mutation):
    broadcast = graphene.Field(BroadcastType)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        if del_obj := Broadcast.objects.last():
            user.broadcast_deleted_upto = del_obj.id
            user.save()
            return DeleteBroadcast(success=True, message="Broadcast has been deleted.")
        else:
            return GraphQLError("There is no Broadcast")


class DeleteChat(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        room_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, root, info, room_id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        room = Room.objects.get(pk=room_id)

        if user not in [room.user_id, room.target]:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed to post or view this chat"))

        if room.deleted in [0, 1] and user == room.user_id:
            room.deleted = 1
            room.save()
        elif room.deleted in [0, 2] and user == room.target:
            room.deleted = 2
            room.save()
        elif room.deleted > 0:
            room.delete()

        return DeleteChat(success=True, message=translate_error_message(info.context.user, "Messages have been deleted."))


class deleteUserMessages(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        message_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, message_id, **kwargs):
        user = info.context.user
        if user is None:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        message = Message.objects.filter(id=int(message_id)).first()
        if message:
            if message.user_id == user or user.roles.filter(role__in=["ADMIN", "CHATTER"]):
                target_user = (
                    message.room_id.target_id
                    if message.user_id == message.room_id.user_id
                    else message.room_id.user_id.id
                )
                # print(f"Target User: {target_user}, room: {message.room_id.id}")
                if message.message_type == "G":
                    raise Exception(translate_error_message(
                        info.context.user, "You cannot delete gift message."))
                message.delete()
                # OnDeleteMessage.broadcast(payload=message_id, group=str(target_user))
                OnDeleteMessage.broadcast(
                    payload=message_id, group=str(message.room_id.id)
                )
                return deleteUserMessages(
                    success=True, message="Messages have been deleted"
                )
            else:
                raise Exception(translate_error_message(
                    info.context.user, "You are not allowed to delete this message"))
        else:
            raise Exception(translate_error_message(
                info.context.user, "Message does not exist."))


class LastSeenMessage(graphene.Mutation):
    message = graphene.Field(MessageType)
    success = graphene.Boolean()

    class Arguments:
        room_id = graphene.Int(required=True)
        # message_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, room_id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception(translate_error_message(
                info.context.user, "You need to be logged in to chat"))

        try:
            room = Room.objects.filter(id=room_id).filter(
                Q(user_id=user) | Q(target=user)
            )
            if not room:
                raise Exception(translate_error_message(
                    info.context.user, "You are not allowed in this Room"))
            room = room[0]
            if user == room.user_id:
                user_for_notification = room.target

            if user == room.target:
                user_for_notification = room.user_id

        except Room.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "Room does not exist"))

        # if message_id:
        #     Message.objects.filter(room_id=room,pk=message_id,read__isnull=True).exclude(user_id=user).update(read=datetime.now())
        # else:
        #     Message.objects.filter(room_id=room,read__isnull=True).exclude(user_id=user).update(read=datetime.now())

        Message.objects.filter(room_id=room, read__isnull=True).exclude(
            user_id=user
        ).update(read=datetime.now())

        try:
            message_seen = (
                Message.objects.filter(room_id=room, read__isnull=False)
                .exclude(user_id=user)
                .first()
            )
            if message_seen is not None:
                OnSeenMessageByReceiver.broadcast(
                    payload=message_seen, group=str(user_for_notification.id)
                )
        except:
            raise Exception(translate_error_message(
                info.context.user, "Error whlie broadcasting lastseen mesage  by receiver"))

        return LastSeenMessage(success=True, message=message_seen)


class OnSeenMessageByReceiver(channels_graphql_ws.Subscription):
    message = graphene.Field(MessageType)
    success = graphene.Boolean()
    notification_queue_limit = 64

    class Arguments:
        token = graphene.String()
        room_id = graphene.Int()

    def subscribe(self, info, token, room_id=None, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        allowed_in_room = Room.objects.filter(id=room_id).filter(
            Q(user_id=user) | Q(target=user)
        )
        if not allowed_in_room:
            raise Exception(translate_error_message(
                info.context.user, "You are not allowed in this Room"))
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info, room_id, token=None, moderator_id=None):
        message_seen = Message.objects.get(id=self.id)

        return OnSeenMessageByReceiver(message=message_seen)


class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()
    create_chat = CreateChat.Field()
    create_notes = CreateNotes.Field()
    sendNotification = SendNotification.Field()
    delete_broadcast = DeleteBroadcast.Field()
    delete_messages = DeleteChat.Field()
    delete_user_messages = deleteUserMessages.Field()
    last_seen_message = LastSeenMessage.Field()
    create_chat_all_moderator = CreateChatAllModerator.Field()
    send_message_all_moderator = SendMessageAllModerator.Field()
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()


class Subscription(graphene.ObjectType):
    on_new_message = OnNewMessage.Field()
    on_delete_message = OnDeleteMessage.Field()
    on_seen_last_message_by_receiver = OnSeenMessageByReceiver.Field()
