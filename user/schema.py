from django_countries import countries
import geopy
import channels_graphql_ws

from django.db.models import fields
from django.db.models.query_utils import subclasses
from graphene_file_upload.scalars import Upload
from django.core.files import File
from framework.api.API_Exception import APIException
import graphene
from user.models import *
from chat.models import Room, Message, Notification, send_notification_fcm, NotificationSettings
from chat.schema import OnNewMessage
from django.db.models import F
# from framework.api.API_Exception import APIException
from gallery.models import Photo
from gallery.schema import PhotoObj
from user import models
from graphene.utils.resolve_only_args import resolve_only_args
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .utils import get_gender_from_code, translate_error_message, get_domain_url_from_context
from datetime import datetime, timedelta
from django.utils import timesince
from django.conf import settings
from django.db import connection as conn
from django.db.models import Q
from .tasks import send_notification_to_nearby_users
from defaultPicker.utils import translated_field_name
from stock_image.models import StockImage


class CoinSettingType(DjangoObjectType):
    class Meta:
        model = models.CoinSettings
        fields = "__all__"


class coinSettingByMethod(graphene.ObjectType):
    method = graphene.String()
    coinsNeeded = graphene.Int()
    region = graphene.String()


class CoinHistoryType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "gift_coins",
            "purchase_coins",
        )


class UserPhotoType(graphene.ObjectType):
    id = graphene.Int()
    url = graphene.String()
    user = graphene.String()
    type = graphene.String()

    def resolve_id(self, info):
        return self.id

    def resolve_url(self, info):
        if self.file:
            try:
                url = info.context.build_absolute_uri(self.file.url)
            except:
                try:
                    domain_url = get_domain_url_from_context(info)
                    if "api.i69app.com" in domain_url:
                        url = settings.DOMAIN_URL + self.file.url
                    else:
                        url = domain_url + self.file.url
                except:
                    url = settings.DOMAIN_URL + self.file.url
            return url
        else:
            return self.file_url

    def resolve_user(self, info):
        return self.user.id

    def resolve_type(self, info):
        if str(self._meta) == "user.userphoto":
            return "PUBLIC"
        elif str(self._meta) == "user.privateuserphoto":
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=self.user,
                requested_user=info.context.user,
                status="A",
                updated_at__gte=datetime.now() - timedelta(hours=hours),
            )
            if request:
                print("REQUEST AVAILABLE")
                return "PUBLIC"
            else:
                print("REQUEST NOT AVAILABLE")
                return "PRIVATE"
        return ""


class Gender(graphene.ObjectType):
    code = graphene.String()
    name = graphene.String()

    def resolve_code(self, info):
        return self

    def resolve_name(self, info):
        return get_gender_from_code(self)


class isOnlineObj(graphene.ObjectType):
    id = graphene.String()
    isOnline = graphene.Boolean()
    username = graphene.String()

    def resolve_isOnline(self, info):
        return self["isOnline"]

    def resolve_username(self, info):
        return self["username"]

    def resolve_id(self, info):
        return self["id"]


class OnlineObj(graphene.ObjectType):
    isOnline = graphene.Boolean()

    def resolve_isOnline(self, info):
        if isinstance(self, User):
            return self.isOnline


# list
class isLastLoginObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    last_login = graphene.String()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_login",
        )


# single
class lastLoginObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    last_login = graphene.String()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_login",
        )


class lastOnlineObj(graphene.ObjectType):
    id = graphene.String()
    last_seen = graphene.String()

    def resolve_last_seen(self, info):
        if self.user_last_seen:
            return timesince.timesince(self.user_last_seen)
        else:
            return timesince.timesince(self.created_at)


class locationDistance(graphene.ObjectType):
    id = graphene.String()
    distance = graphene.String()

    def resolve_distance(self, info):
        user1_location = info.context.user.location
        user2_location = self.location
        if user1_location and user2_location:
            try:
                distance = geopy.distance.geodesic(
                    user1_location.split(","), user2_location.split(",")
                ).km
                return f"{round(distance, 2)} Km"
            except:
                return "Location Undetermined."
        elif not user1_location:
            return "Location Undetermined."
            # raise Exception("Your location is not added.")
        elif not user2_location:
            return "Location Undetermined."
            # raise Exception(f'{self.fullName} has not entered their location.')


class UploadFileObj(graphene.ObjectType):
    id = graphene.String()
    success = graphene.Boolean()
    image_data = graphene.String()


class coinsResponseObj(graphene.ObjectType):
    id = graphene.String()
    coins = graphene.Int()
    success = graphene.Boolean()


class blockResponseObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    success = graphene.Boolean()


class updateCoin(graphene.Mutation):
    class Arguments:
        coins = graphene.Int()
        id = graphene.String()

    Output = coinsResponseObj

    def mutate(self, info, coins=None, id=None):
        user = User.objects.get(id=id)
        coin = user.coins
        print(coin)

        if coins is not None:
            user = user.addCoins(coins)

        user.save()
        return coinsResponseObj(id=user.id, success=True, coins=user.coins)


class privateUserPhotos(DjangoObjectType):
    class Meta:
        model = PrivateUserPhoto
        fields = ("id", "file")

    def resolve_file(self, obj):
        return self.file.url


class createPrivatePhotosMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=False)
        user_id = graphene.String(required=False)
        stock_image_id = graphene.Int(required=False)

    obj = graphene.Field(privateUserPhotos)

    def mutate(self, info, file=None, user_id=None, stock_image_id=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception(translate_error_message(
                info.context.user, "You must be logged in to perform this action."))
        if user_id and user.roles.filter(role=UserRole.ROLE_ADMIN).exists():
            user = User.objects.get(id=user_id)
        if stock_image_id:
            try:
                file = StockImage.objects.get(id=stock_image_id).file
            except:
                return Exception(translate_error_message(info.context.user, "Invalid stock Image Id"))
        private_photo = PrivateUserPhoto.objects.create(file=file, user=user)
        return createPrivatePhotosMutation(obj=private_photo)


class requestUserPrivatePhotosMutation(graphene.Mutation):
    msg = graphene.String()

    class Arguments:
        receiver_id = graphene.String(required=True)

    def mutate(self, info, receiver_id):
        user_obj = info.context.user
        receiver_obj = User.objects.filter(id=receiver_id).first()
        print(user_obj, receiver_obj)

        # CREATE REQUEST OBJECT
        request = PrivatePhotoViewRequest.objects.create(
            user_to_view=receiver_obj, requested_user=user_obj, status="P"
        )

        # IF NO CHAT CREATE ROOM
        room_name_a = [user_obj.username, receiver_obj.username]
        room_name_a.sort()
        room_name_str = room_name_a[0] + "_" + room_name_a[1]

        try:
            chat_room = Room.objects.get(name=room_name_str)
        except Room.DoesNotExist:
            chat_room = Room(name=room_name_str,
                             user_id=user_obj, target=receiver_obj)
            chat_room.save()

        chat_room.last_modified = datetime.now()
        chat_room.save()

        # DEDUCTING COINS
        coins = CoinSettings.objects.filter(
            method="REQUEST_PRIVATE_ALBUM").first()
        coins_for_region = CoinSettingsForRegion.objects.filter(
            coinsettings=coins, region=user_obj.get_coinsettings_region()
        )
        if coins_for_region.count():
            coins = coins_for_region.first()

        if coins:
            if user_obj.gift_coins + user_obj.purchase_coins < coins.coins_needed:
                return requestUserPrivatePhotosMutation(
                    msg="Insufficient coins: {} coins required".format(
                        coins.coins_needed
                    )
                )
            if coins.coins_needed > 0:
                user_obj.deductCoins(coins.coins_needed,
                                     "REQUEST_PRIVATE_ALBUM")
                user_obj.save()

        # CREATE MESSAGE
        message = Message.objects.create(
            room_id=chat_room,
            user_id=user_obj,
            content=f"{user_obj.fullName} requested to view your private album.",
            message_type="P",
            private_photo_request_id=request.id,
        )
        # SEND NOTIFICATION.
        notification_setting = "SNDMSG"
        # checks for avatar_url if None
        try:
            avatar_url = user_obj.avatar().file.url
        except:
            avatar_url = None
        data = {
            "roomID": chat_room.id,
            "notification_type": notification_setting,
            "message": message.content,
            "user_avatar": avatar_url,
            "title": "Sent message",
        }
        icon = None
        if avatar_url:
            icon = info.context.build_absolute_uri(avatar_url)
        android_channel_id = None
        notification_obj = Notification(
            user=receiver_obj,
            sender=None,
            app_url=None,
            notification_setting_id=notification_setting,
            data=data,
            priority=None,
        )
        send_notification_fcm(
            notification_obj=notification_obj,
            android_channel_id=android_channel_id,
            icon=icon,
            image=icon,
        )
        OnNewMessage.broadcast(payload=message, group=str(chat_room.id))
        return requestUserPrivatePhotosMutation(msg="Request has been created.")


class cancelPrivatePhotoRequest(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        user_id = graphene.String(required=True)

    def mutate(self, info, user_id):
        user_obj = info.context.user
        profile_user = User.objects.get(id=user_id)

        request = (
            PrivatePhotoViewRequest.objects.filter(
                user_to_view=profile_user,
                requested_user=user_obj,
            )
            .order_by("-id")
            .first()
        )
        if request:
            # CHAT ROOM
            room_name_a = [user_obj.username, profile_user.username]
            room_name_a.sort()
            room_name_str = room_name_a[0] + "_" + room_name_a[1]

            try:
                chat_room = Room.objects.get(name=room_name_str)
            except Room.DoesNotExist:
                chat_room = Room(
                    name=room_name_str, user_id=user_obj, target=request.requested_user
                )
                chat_room.save()

                chat_room.last_modified = datetime.now()
                chat_room.save()
            message = Message.objects.create(
                room_id=chat_room,
                user_id=request.requested_user,
                content=f"{request.user_to_view.fullName} cancelled the request",
                message_type="CM",
            )
            request.status = "C"
            request.save()
            OnUpdatePrivateRequest.broadcast(
                group=None,
                payload={
                    "user_to_view": str(profile_user.id),
                    "requested_user": str(user_obj.id),
                    "status": request.status,
                },
            )
            return cancelPrivatePhotoRequest(message="Request Cancelled")


class privatePhotoDecision(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        request_id = graphene.Int()
        decision = graphene.String()

    def mutate(self, info, request_id, decision):
        user_obj = info.context.user
        request = PrivatePhotoViewRequest.objects.filter(id=request_id).first()
        if request and decision in ["A", "R", "C"]:
            if (
                request.user_to_view == user_obj
                or user_obj.roles.filter(
                    Q(role=UserRole.ROLE_ADMIN) | Q(
                        role=UserRole.ROLE_FAKE_USER)
                ).exists()
            ):
                # CHAT ROOM
                room_name_a = [
                    request.user_to_view.username,
                    request.requested_user.username,
                ]
                room_name_a.sort()
                room_name_str = room_name_a[0] + "_" + room_name_a[1]

                try:
                    chat_room = Room.objects.get(name=room_name_str)
                except Room.DoesNotExist:
                    chat_room = Room(
                        name=room_name_str,
                        user_id=request.user_to_view,
                        target=request.requested_user,
                    )
                    chat_room.save()

                chat_room.last_modified = datetime.now()
                chat_room.save()
                if decision == "A":
                    message = Message.objects.create(
                        room_id=chat_room,
                        user_id=request.user_to_view,
                        content=f"{request.user_to_view.fullName} approved {request.requested_user.fullName} request",
                        message_type="CM",
                    )
                    request.status = "A"
                    send_notification = True
                elif decision == "R":
                    message = Message.objects.create(
                        room_id=chat_room,
                        user_id=request.user_to_view,
                        content=f"{request.user_to_view.fullName} rejected {request.requested_user.fullName} request",
                        message_type="CM",
                    )
                    request.status = "R"
                    send_notification = True
                else:
                    message = Message.objects.create(
                        room_id=chat_room,
                        user_id=request.requested_user,
                        content=f"{request.user_to_view.fullName} cancelled the request",
                        message_type="CM",
                    )
                    request.status = "C"
                    send_notification = False
                request.save()
                OnNewMessage.broadcast(
                    payload=message, group=str(chat_room.id))
                OnUpdatePrivateRequest.broadcast(
                    group=None,
                    payload={
                        "user_to_view": str(request.user_to_view.id),
                        "requested_user": str(request.requested_user.id),
                        "status": request.status,
                    },
                )
                if send_notification:
                    notification_setting = "SNDMSG"
                    # checks for avatar_url if None
                    try:
                        avatar_url = request.user_to_view.avatar().file.url
                    except:
                        avatar_url = None
                    data = {
                        "roomID": chat_room.id,
                        "notification_type": notification_setting,
                        "message": message.content,
                        "user_avatar": avatar_url,
                        "title": "Sent message",
                    }
                    icon = None
                    if avatar_url:
                        icon = info.context.build_absolute_uri(avatar_url)
                    android_channel_id = None
                    notification_obj = Notification(
                        user=request.requested_user,
                        sender=None,
                        app_url=None,
                        notification_setting_id=notification_setting,
                        data=data,
                        priority=None,
                    )
                    send_notification_fcm(
                        notification_obj=notification_obj,
                        android_channel_id=android_channel_id,
                        icon=icon,
                        image=icon,
                    )

                return privatePhotoDecision(success=True)
            else:
                return Exception(translate_error_message(info.context.user, "You are not allowed to approve this request."))

        else:
            return Exception(translate_error_message(info.context.user, "Invalid Request"))


class ChatCoin(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        method = graphene.String()

    Output = coinsResponseObj

    def mutate(self, info, method=None, id=None):
        user = User.objects.get(id=id)
        if user.is_anonymous:
            return APIException(translate_error_message(info.context.user, "You must be logged in to use coins"))
        coin = user.coins
        print(coin)
        # if method.upper() == "MESSAGE":
        #     user = user.deductCoin(19)

        # elif method.upper() == "IMAGE_MESSAGE":
        #     user = user.deductCoin(60)

        coin_settings = CoinSettings.objects.all()
        for coin_setting in coin_settings:
            if method.upper() == coin_setting.method.upper():
                coinsettings_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coin_setting, region=user.get_coinsettings_region()
                )
                if coinsettings_for_region.count():
                    coin_setting = coinsettings_for_region.first()

                if coin < coin_setting.coins_needed:
                    return APIException(translate_error_message(info.context.user, "Insufficient Coins"))
                user.deductCoins(coin_setting.coins_needed, method.upper())
                break
        else:
            return APIException(translate_error_message(info.context.user, "Please enter a valid method"))
        if method.upper() == "PROFILE_PICTURE":
            user.photos_quota += 1
        user.save()
        return coinsResponseObj(id=user.id, success=True, coins=user.coins)


# class UpdateProfilePic(graphene.Mutation):
#     Output = UploadFileObj

#     class Arguments:
#         id = graphene.String()
#         image_data = graphene.String()

#     def mutate(self, info,  id=None, image_data=None):
#         user = User.objects.get(id=id)
#         avatar = image_data
#         user.avatar = avatar
#         user.save()
#         return UploadFileObj(id=user.id, image_data=user.avatar, success=True)


class MutationResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()


class DeleteAvatarPhoto(graphene.Mutation):
    Output = MutationResponse

    class Arguments:
        id = graphene.String(required=True)
        moderator_id = graphene.String()

    def mutate(self, info, id=None, moderator_id=None):
        current_user = info.context.user
        if not id:
            return MutationResponse(success=False, message="Id is required")

        if not current_user.is_authenticated:
            return MutationResponse(success=False, message="Authentication required")

        try:
            photo = models.UserPhoto.objects.get(id=id)
        except models.UserPhoto.DoesNotExist:
            return MutationResponse(success=False, message="Image not found")

        if models.UserPhoto.objects.filter(user=photo.user).count() == 1:
            return MutationResponse(success=False, message="You cannot delete your only public photo")

        if moderator_id:
            fake_user = current_user.fake_users.all()

            if fake_user.count() > 0:
                if fake_user.filter(id=moderator_id).count() > 0:
                    photo.delete()
                    return MutationResponse(
                        success=True,
                    )
                else:
                    return MutationResponse(
                        success=False,
                        message="You are not authorized to delete this image",
                    )

        roles = {r.role for r in current_user.roles.all()}
        photo_user_roles = {r.role for r in photo.user.roles.all()}
        if "MODERATOR" in photo_user_roles and "ADMIN" in roles:
            pass
        elif photo.user.id != current_user.id and "ADMIN" not in roles:
            return MutationResponse(
                success=False, message="You are not authorized to delete this image"
            )

        photo.delete()
        return MutationResponse(
            success=True,
        )


class DeletePrivatePhoto(graphene.Mutation):
    Output = MutationResponse

    class Arguments:
        id = graphene.String(required=True)
        moderator_id = graphene.String()

    def mutate(self, info, id=None, moderator_id=None):
        user = info.context.user
        print(user)
        if not id:
            return MutationResponse(success=False, message="Id is required")

        if not user.is_authenticated:
            return MutationResponse(success=False, message="Authentication required")

        photos = models.PrivateUserPhoto.objects.filter(id=id)

        if photos.count() == 0:
            return MutationResponse(success=False, message="Image not found")

        photo = photos[0]

        if moderator_id:
            fake_user = user.fake_users.all()

            if fake_user.count() > 0:
                if fake_user.filter(id=moderator_id).count() > 0:
                    photo.delete()
                    return MutationResponse(
                        success=True,
                    )
                else:
                    return MutationResponse(
                        success=False,
                        message="You are not authorized to delete this image",
                    )

        if photo.user.id != user.id:
            return MutationResponse(
                success=False, message="You are not authorized to delete this image"
            )

        photo.delete()
        return MutationResponse(
            success=True,
        )


class blockUser(graphene.Mutation):
    Output = blockResponseObj

    class Arguments:
        id = graphene.String()
        blocked_id = graphene.String()

    def mutate(self, info, id, blocked_id):
        try:
            blckd_user = User.objects.get(id=blocked_id)
            user = User.objects.get(id=id)
        except Exception as e:
            raise Exception(translate_error_message(
                info.context.user, f"User does not exist"))
        if user == blckd_user:
            raise Exception(translate_error_message(
                info.context.user, "You can not block yourself"))
        user.blockedUsers.add(blckd_user)
        user.save()

        return blockResponseObj(
            id=blckd_user.id, username=blckd_user.username, success=True
        )


class unblockUser(graphene.Mutation):
    Output = blockResponseObj

    class Arguments:
        id = graphene.String()
        blocked_id = graphene.String()

    def mutate(self, info, id, blocked_id):
        blckd_user = User.objects.get(id=blocked_id)
        user = User.objects.get(id=id)
        print("======================")
        print(user.blockedUsers)
        print("======================")
        user.blockedUsers.remove(blckd_user)
        user.save()

        return blockResponseObj(
            id=blckd_user.id, username=blckd_user.username, success=True
        )


class FollowType(DjangoObjectType):
    class Meta:
        model = ProfileFollow
        fields = "__all__"


class ProfileVisitType(DjangoObjectType):
    datetime = graphene.Field(graphene.String, resolver=lambda profilevisit,
                              info: f"{profilevisit.created_at.date()}/{profilevisit.created_at.time().hour}")
    # hour = graphene.Field(graphene.String , resolver = lambda profilevisit , info:)
    # new_filed = graphene.Field(graphene.String, resolver = lambda profilevisit, str(hour) + "/" + str(date))

    class Meta:
        model = ProfileVisit
        fields = ("id", "visitor", "visiting", "datetime")


class UserFollowMutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        user_id = graphene.ID(required=True)

    profile_follow = graphene.Field(FollowType)

    @classmethod
    def mutate(cls, root, info, user_id):
        follower_user = info.context.user
        try:
            following_user = User.objects.get(id=user_id)
        except:
            raise Exception(translate_error_message(
                info.context.user, "Invalid User ID"))
        if follower_user.id == following_user.id:
            raise Exception(translate_error_message(
                info.context.user, "User cannot follow itself"))
        follow_obj, created = ProfileFollow.objects.get_or_create(
            follower=follower_user, following=following_user)
        priority = None
        icon = None
        app_url = None
        android_channel_id = None
        notification_setting = "USERFOLLOW"
        data = {
            "followerID": str(follower_user.id),
            "notification_type": notification_setting
        }
        notification_obj = Notification(
            user=following_user,
            sender=follower_user,
            app_url=app_url,
            notification_setting_id=notification_setting,
            data=data,
            priority=priority,
        )
        send_notification_fcm(
            notification_obj=notification_obj,
            android_channel_id=android_channel_id,
            icon=icon,
        )
        user_followers = ProfileFollow.objects.filter(
            ~Q(follower=following_user),
            following=follower_user)
        if user_followers.exists():
            for user_follower in user_followers:
                notification_obj = Notification(
                    user=user_follower.follower,
                    sender=follower_user,
                    app_url=app_url,
                    notification_setting_id=notification_setting,
                    data=data,
                    priority=priority,
                )
                send_notification_fcm(
                    notification_obj=notification_obj,
                    android_channel_id=android_channel_id,
                    icon=icon,
                )

        if created:
            FollowSubscription.broadcast(
                group='follow_subscription',
                payload={'profile_follow_instance': follow_obj}
            )
        return UserFollowMutation(profile_follow=follow_obj)


class UserUnFollowMutation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        # user=graphene.String(required=True)
        user_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, user_id):
        follower_user = info.context.user
        try:
            following_user = User.objects.get(id=user_id)
        except:
            raise Exception(translate_error_message(
                info.context.user, "Invalid User ID"))
        if follower_user.id == following_user.id:
            raise Exception(translate_error_message(
                info.context.user, "User cannot unfollow itself"))
        try:
            follow_obj = ProfileFollow.objects.get(
                follower=follower_user, following=following_user)
            follow_obj.delete()
        except:
            raise Exception(translate_error_message(
                info.context.user, "Unable to unfollow User! User should be followed first."))
        return UserUnFollowMutation(message=translate_error_message(info.context.user, "User has been unfollowed"))


class UserRemoveFollowerMutation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        # user=graphene.String(required=True)
        user_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, user_id):
        following_user = info.context.user
        try:
            follower_user = User.objects.get(id=user_id)
        except:
            raise Exception("Invalid User ID")
        if following_user.id == follower_user.id:
            raise Exception("User cannot remove itself")
        try:
            follow_obj = ProfileFollow.objects.get(
                follower=follower_user, following=following_user)
            follow_obj.delete()
        except:
            raise Exception(translate_error_message(
                info.context.user, "Unable to remove User! User should be follower first."))
        return UserUnFollowMutation(message=translate_error_message(info.context.user, "User has been removed from your followers List"))


class blockedUsers(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()

    def resolve_id(self, info):
        return self["id"]

    def resolve_username(self, info):
        return self["username"]


class TestNoteType(graphene.ObjectType):
    message = graphene.String()


class DeleteAccountAllowed(DjangoObjectType):
    class Meta:
        model = DeleteAccountSetting
        fields = "__all__"


class UserInterestType(DjangoObjectType):
    class Meta:
        model = UserInterestedIn
        fields = "__all__"

    def resolve_str_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "str_name"))


class CountryType(DjangoObjectType):
    full_name = graphene.String()

    class Meta:
        model = Country
        fields = "__all__"

    def resolve_full_name(self, info):
        for country in list(countries):
            if country[0] == self.name:
                return country[1]

        return self.name


class UserHideInterestType(DjangoObjectType):
    class Meta:
        model = HideUserInterestedIn
        fields = "__all__"


class UserInterestForRegionType(DjangoObjectType):
    class Meta:
        model = UserInterestForRegion
        fields = "__all__"


class UserProfileTranslationType(DjangoObjectType):
    class Meta:
        model = UserProfileTranlations
        fields = "__all__"


class Query(graphene.ObjectType):

    usersOnline = graphene.List(isOnlineObj)
    isOnline = graphene.Field(OnlineObj, id=graphene.String(required=True))
    delete_account_allowed = graphene.List(DeleteAccountAllowed)

    inactiveUsers = graphene.List(
        isLastLoginObj,
        from_time=graphene.String(required=True),
        to_time=graphene.String(required=True),
    )
    lastLogin = graphene.Field(lastLoginObj, id=graphene.String(required=True))
    lastOnline = graphene.Field(
        lastOnlineObj, id=graphene.String(required=True))
    user_location = graphene.Field(
        locationDistance, id=graphene.String(required=True))

    private_user_photos = graphene.List(
        privateUserPhotos, id=graphene.String(required=True)
    )

    blockedUsers = graphene.List(blockedUsers)

    coinSettings = graphene.List(CoinSettingType)
    coinSettingByMethod = graphene.Field(
        coinSettingByMethod, method=graphene.String())

    test_notification = graphene.Field(TestNoteType)

    user_interests = graphene.List(UserInterestType)
    all_countries = graphene.List(CountryType)

    # depricated
    # photos = graphene.List(PhotoObj, id=graphene.String(required=True))

    def resolve_private_user_photos(self, info, **kwargs):
        user_obj = info.context.user
        user_to_view = User.objects.get(id=kwargs["id"])

        if (
            user_obj == user_to_view
            or user_obj.roles.filter(role=UserRole.ROLE_ADMIN).exists()
        ):
            return PrivateUserPhoto.objects.filter(user=user_to_view)
        else:
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=user_to_view,
                requested_user=user_obj,
                status="A",
                updated_at__gte=datetime.now() - timedelta(hours=hours),
            )
            if request:
                return PrivateUserPhoto.objects.filter(user=user_to_view)
            else:
                return PrivateUserPhoto.objects.none()

    def resolve_usersOnline(self, info):
        try:
            return User.objects.filter(isOnline=True).values(
                "isOnline", "username", "id"
            )
        except:
            raise Exception("try again")

    def resolve_isOnline(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            user = User.objects.get(id=id)
            return user
        else:
            raise Exception(translate_error_message(
                info.context.user, "Id is a required parameter"))

    def resolve_lastLogin(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception(translate_error_message(
                    info.context.user, "User not found"))

            return user
        else:
            raise Exception(translate_error_message(
                info.context.user, "Id is a required parameter"))

    def resolve_lastOnline(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception(translate_error_message(
                    info.context.user, "User not found"))

            return user
        else:
            raise Exception(translate_error_message(
                info.context.user, "Id is a required parameter"))

    def resolve_user_location(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception(translate_error_message(
                    info.context.user, "User not found"))

            return user
        else:
            raise Exception(translate_error_message(
                info.context.user, "Id is a required parameter"))

    def resolve_inactiveUsers(self, info, from_time="0.5", to_time="1"):
        """
        from_time and to_time is float
        30 minutes to 1 hour => 0.5 - 1
        1 hour to 5 hours => 1 - 5
        ...
        """
        try:
            from2 = float(from_time)
        except ValueError:
            raise Exception(translate_error_message(
                info.context.user, "from_time needs to be a number of hours. can be float."))

        try:
            to2 = float(to_time)
        except ValueError:
            raise Exception(translate_error_message(
                info.context.user, "to_time needs to be a number of hours. can be float."))

        if float(from_time) > float(to_time):
            raise Exception(translate_error_message(
                info.context.user, "from_time cant be greater than to_time"))

        if float(from_time) < 1:
            from_time = float(from_time) * 60
            from_time = datetime.today() - timedelta(hours=0, minutes=int(from_time))
        elif float(from_time) >= 1 and float(from_time) <= 24:
            minutes = 0
            if float(from_time) != int(from_time):
                minutes = int((float(from_time) - int(from_time)) * 60)
            from_time = datetime.today() - timedelta(
                hours=int(from_time), minutes=int(minutes)
            )
        else:
            from_time = int(from_time) / 24
            hours = 0
            if float(from_time) != int(from_time):
                hours = int((float(from_time) - int(from_time)) * 24)
            from_time = datetime.today() - timedelta(
                days=int(from_time), hours=int(hours)
            )

        if float(to_time) < 1:
            to_time = float(to_time) * 60
            to_time = datetime.today() - timedelta(hours=0, minutes=int(to_time))
        elif float(to_time) >= 1 and float(to_time) <= 24:
            minutes = 0
            if float(to_time) != int(to_time):
                minutes = int((float(to_time) - int(to_time)) * 60)
            to_time = datetime.today() - timedelta(
                hours=int(to_time), minutes=int(minutes)
            )
        else:
            to_time = float(to_time) / 24
            hours = 0
            if float(to_time) != int(to_time):
                hours = int((float(to_time) - int(to_time)) * 24)
            to_time = datetime.today() - timedelta(days=int(to_time), hours=int(hours))
        try:
            from_time = from_time.strftime("%Y-%m-%d %H:%M:%S")
            to_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
            users = User.objects.filter(last_login__range=(to_time, from_time)).values(
                "id", "username", "last_login"
            )
            return users
        except Exception as e:
            raise Exception(translate_error_message(
                info.context.user, "try again"), e)

    def resolve_blockedUsers(self, info):
        id = info.context.user.id
        user = User.objects.get(id=id)
        return user.blockedUsers.all().values("id", "username")

    def resolve_coinSettings(self, info):
        return CoinSettings.objects.all()

    def resolve_coinSettingByMethod(self, info, method=None, **kwargs):
        user = info.context.user
        response_obj = CoinSettingsForRegion.objects.filter(
            region=user.get_coinsettings_region())
        if method is None:
            raise Exception("method is a required parameter")
        return_obj = {'coinsNeeded': None, 'region': None, 'method': None}
        for obj in response_obj:
            if obj.coinsettings.method == method:
                return_obj['coinsNeeded'] = obj.coins_needed
                return_obj['region'] = obj.region
                return_obj['method'] = obj.coinsettings.method
        return return_obj

    def resolve_delete_account_allowed(self, info):
        return DeleteAccountSetting.objects.all()

    # depricated
    # def resolve_photos(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     if id is None:
    #         return Exception("Id is a required parameter")
    #     user = get_user_model().objects.get(id=id)
    #     return Photo.objects.filter(user=user)

    def resolve_test_notification(self, info):
        send_notification_to_nearby_users.apply_async(
            args=[str(info.context.user.id)])
        return TestNoteType(message="Success")

    def resolve_user_interests(self, info):
        user_obj = info.context.user
        return UserInterestedIn.objects.select_related().filter(
            Q(userinterestforregion__region__countries__name__iexact=user_obj.country_code)
        ).order_by('-created_at').distinct()

    def resolve_all_countries(self, info):
        return Country.objects.all()


class OnUpdatePrivateRequest(channels_graphql_ws.Subscription):

    user_to_view = graphene.String()
    requested_user = graphene.String()
    status = graphene.String()

    class Arguments:
        user_to_view = graphene.String()
        requested_user = graphene.String()
        status = graphene.String()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        user_to_view = self["user_to_view"]
        requested_user = self["requested_user"]
        status = self["status"]
        print("******************{}***************".format(user_to_view))
        print("******************{}***************".format(requested_user))
        return OnUpdatePrivateRequest(
            user_to_view=user_to_view, requested_user=requested_user, status=status
        )


class FollowSubscription(channels_graphql_ws.Subscription):
    profile_follow = graphene.Field(FollowType)

    class Meta:
        description = 'Subscription for ProfileFollow'

    def subscribe(root, info):
        return ["follow_subscription"]

    @classmethod
    @staticmethod
    def publish(payload, info):
        return FollowSubscription(profile_follow=payload['profile_follow_instance'])


class ProfileVisitSubscription(channels_graphql_ws.Subscription):
    profile_visit = graphene.Field(ProfileVisitType)

    class Meta:
        description = 'Subscription for ProfileVisit'

    @staticmethod
    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    @staticmethod
    def publish(payload, info):
        return ProfileVisitSubscription(profile_visit=payload['profile_visit_instance'])

    @classmethod
    def broadcast(cls, group=None, payload=None):
        if type(payload) is not dict:
            payload = {"profile_visit_instance": payload}
        return super().broadcast(group=group, payload=payload)



class HideInterestedInSubscription(channels_graphql_ws.Subscription):
    user_interestedIn_region = graphene.Field(UserInterestForRegionType)

    class Meta:
        description = 'Subscription for Hiding Interested In option'

    def subscribe(root, info):
        return ["hide_interested_in_subscription"]

    @classmethod
    @staticmethod
    def publish(payload, info):
        return HideInterestedInSubscription(user_interestedIn_region=payload['user_interestedIn_instance'])


class UserProfileTranslationSubscription(channels_graphql_ws.Subscription):
    user_profile_translation = graphene.Field(UserProfileTranslationType)

    class Meta:
        description = 'Subscription for User Profile Translation'

    def subscribe(root, info):
        return ["user_profile_translation_subscription"]

    @classmethod
    @staticmethod
    def publish(payload, info):
        return UserProfileTranslationSubscription(user_profile_translation=payload['user_profile_translation_instance'])


class OnUserOnline(channels_graphql_ws.Subscription):
    id = graphene.String()
    username = graphene.String()
    full_name = graphene.String()
    relation_type = graphene.String()

    class Arguments:
        pass

    class Meta:
        description = 'Subscription for user being followed comes online'

    def subscribe(cls, info):
        user = info.context.user
        return [f"online_{user.id}"] if user is not None and user.is_authenticated else []

    def publish(self, info):
        id_ = self["id"]
        username = self["username"]
        full_name = self["full_name"]
        relation_type = self["relation_type"]
        return OnUserOnline(
            id=id_, username=username, full_name=full_name, relation_type=relation_type
        )

    @classmethod
    def notify_related_users(cls, user):
        follower_ids = models.ProfileFollow.objects.filter(
            following_id=user.id
        ).values_list("follower_id", flat=True)
        followers = models.User.objects.filter(
            id__in=follower_ids
        )

        for follower in followers or []:
            cls.broadcast(
                group=f"online_{follower.id}",
                payload={
                    "id": str(follower.id),
                    "username": follower.username,
                    "relation_type": "Following",
                    "full_name": follower.fullName,
                },
            )


class Mutation(graphene.ObjectType):
    updateCoin = updateCoin.Field()
    # depricated
    # UpdateProfilePic = UpdateProfilePic.Field()
    deleteAvatarPhoto = DeleteAvatarPhoto.Field()
    deletePrivatePhoto = DeletePrivatePhoto.Field()
    createPrivatePhoto = createPrivatePhotosMutation.Field()
    requestUserPrivatePhotos = requestUserPrivatePhotosMutation.Field()
    cancelPrivatePhotoRequest = cancelPrivatePhotoRequest.Field()
    privatePhotoDecision = privatePhotoDecision.Field()
    blockUser = blockUser.Field()
    unblockUser = unblockUser.Field()
    deductCoin = ChatCoin.Field()
    user_follow = UserFollowMutation.Field()
    user_unfollow = UserUnFollowMutation.Field()
    user_remove_follower = UserRemoveFollowerMutation.Field()


class Subscription(graphene.ObjectType):
    on_update_private_request = OnUpdatePrivateRequest.Field()
    follow_subscription = FollowSubscription.Field()
    profile_visit_subscription = ProfileVisitSubscription.Field()
    hide_interested_in_subscription = HideInterestedInSubscription.Field()
    user_profile_translation_subscription = UserProfileTranslationSubscription.Field()
    related_user_online = OnUserOnline.Field()
