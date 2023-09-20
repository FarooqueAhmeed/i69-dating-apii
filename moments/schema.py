import datetime
import mimetypes
import traceback
from datetime import datetime, timedelta
from itertools import chain

import channels_graphql_ws
import graphene
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django_filters import CharFilter, FilterSet
from googletrans import Translator
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_file_upload.scalars import Upload
from rest_framework.authtoken.models import Token
from stock_image.models import StockImage
from chat.models import Notification, send_notification_fcm, NotificationSettings
from defaultPicker.utils import custom_translate
from moments.utils import (
    all_user_multi_stories_query,
    detect_moment,
    detect_story,
    modify_text,
    get_worker_user
)
from user.models import PrivatePhotoViewRequest, PrivatePhotoViewTime, UserLimit, ProfileFollow, ChatsQue
from user.schema import UserPhotoType
from user.utils import translate_error_message

from .models import *
from .tasks import createThumbnail

EXPIRE_TIME = 24  # hours
translator = Translator()
from purchase.decorators import check_permission


class UserTypeone(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)

    avatar_photos = graphene.List(UserPhotoType)
    avatar = graphene.Field(UserPhotoType)
    private_photo_request_status = graphene.String()

    def resolve_avatar(self, info):
        return self.avatar()

    def resolve_avatar_photos(self, info):
        print("WORKING")
        return list(chain(self.avatar_photos.all(), self.private_avatar_photos.all()))

    def resolve_private_photo_request_status(self, info):
        if info.context.user == self:
            return ""
        else:
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=self.user,
                requested_user=info.context.user,
                updated_at__gte=datetime.now() - timedelta(hours=hours),
            )
            if request.status == "P":
                return "Cancel Request"
            else:
                return "Request Access"


class GenericLikeType(DjangoObjectType):
    pk = graphene.Int(source="pk")

    class Meta:
        model = GenericLike
        filter_fields = {}
        fields = "__all__"
        interfaces = (relay.Node,)


class GenericReplyType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    likes = DjangoFilterConnectionField(GenericLikeType)
    likes_count = graphene.Int()

    class Meta:
        model = GenericComment
        filter_fields = {}
        fields = "__all__"
        interfaces = (relay.Node,)

    def resolve_likes_count(self, info):
        return self.likes.all().count()


class GenericCommentType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    replys = DjangoFilterConnectionField(GenericReplyType)
    likes = DjangoFilterConnectionField(GenericLikeType)
    likes_count = graphene.Int()

    class Meta:
        model = GenericComment
        filter_fields = {}
        fields = "__all__"
        interfaces = (relay.Node,)

    def resolve_replys(self, info):
        ct = ContentType.objects.get(app_label="moments", model="genericcomment")
        return GenericComment.objects.filter(
            object_id=self.id, content_type=ct
        ).order_by("-created_date")

    def resolve_likes_count(self, info):
        return self.likes.all().count()


class ReplyType(DjangoObjectType):
    class Meta:
        model = Comment
        filter_fields = ("reply_to",)
        fields = (
            "id",
            "user",
            "momemt",
            "comment_description",
            "created_date",
            "reply_to",
        )
        interfaces = (relay.Node,)


class CommentFilter(FilterSet):
    pk = CharFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Comment
        fields = [
            "momemt__id",
            "id",
        ]

    @property
    def qs(self):
        # The query context can be found in self.request.
        return (
            super(CommentFilter, self)
            .qs.filter(reply_to=None)
            .order_by("-created_date")
        )


class CommentType(DjangoObjectType):
    pk = graphene.Int(source="pk")

    class Meta:
        model = Comment
        fields = ("id", "user", "momemt", "comment_description", "created_date")
        filterset_class = CommentFilter
        interfaces = (relay.Node,)

    # replys = DjangoFilterConnectionField(ReplyType)
    replys = graphene.List(ReplyType)
    like = graphene.Int()
    report = graphene.Int()

    def resolve_like(self, info):
        return CommentLike.objects.filter(comment=self).count()

    def resolve_replys(self, info):
        return Comment.objects.filter(reply_to=self).order_by("-created_date")

    def resolve_report(self, info):
        return ReportComment.objects.filter(comment=self).count()


class MomentFilter(FilterSet):
    pk = CharFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Moment
        fields = [
            "user__id",
            "id",
        ]

    @property
    def qs(self):
        # The query context can be found in self.request.
        return super(MomentFilter, self).qs.order_by("-created_date")


class UserStories(DjangoObjectType):

    likes = graphene.List(GenericLikeType)

    class Meta:
        model = Story
        fields = ("user__id", "created_date", "file", "thumbnail", "likes", "comments")
        interfaces = (relay.Node,)

    def resolve_likes(self, args):
        return self.likes.all()


class MomentsTyps(DjangoObjectType):
    pk = graphene.Int(source="pk")

    class Meta:
        model = Moment
        fields = ("id", "Title", "file", "created_date", "user", "moment_description")
        filterset_class = MomentFilter
        interfaces = (relay.Node,)

    user = graphene.Field(UserTypeone)
    like = graphene.Int()
    comment = graphene.Int()
    moment_description_paginated = graphene.List(
        graphene.String, width=graphene.Int(), character_size=graphene.Int()
    )

    def resolve_moment_description_paginated(
        self, info, width=None, character_size=None
    ):

        try:
            max_length = int(width / character_size)

            description_length = len(self.moment_description)

            if max_length >= description_length:
                return [self.moment_description]
            char = None
            while max_length > 0:

                if char == " ":
                    max_length = max_length + 1

                    break
                char = self.moment_description[max_length]
                max_length = max_length - 1
            desc_list = []
            desc_list.append(f"{self.moment_description[0:max_length]}")
            desc_list.append(
                self.moment_description[max_length : description_length - 1]
            )
            return desc_list
        except Exception as e:
            print(e)
            return [self.moment_description]

    def resolve_like(self, info):
        return Like.objects.filter(momemt=self).count()

    def resolve_comment(self, info):
        return Comment.objects.filter(momemt=self, reply_to=None).count()


class StoryFilter(FilterSet):
    pk = CharFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Story
        fields = [
            "user__id",
            "id",
        ]

    @property
    def qs(self):
        # The query context can be found in self.request.
        try:
            visible_time = StoryVisibleTime.objects.all().first()
            hours = (
                visible_time.hours
                + visible_time.days * 24
                + visible_time.weeks * 7 * 24
            )

        except:
            hours = 24
        return (
            super(StoryFilter, self)
            .qs.filter(
                created_date__gte=datetime.datetime.now()
                - datetime.timedelta(hours=hours)
            )
            .order_by("-created_date")
        )


class StoryType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    likes = DjangoFilterConnectionField(GenericLikeType)
    likes_count = graphene.Int()
    comments_count = graphene.Int()
    comments = DjangoFilterConnectionField(GenericCommentType)

    class Meta:
        model = Story
        fields = "__all__"
        interfaces = (relay.Node,)
        filterset_class = StoryFilter

    user = graphene.Field(UserTypeone)
    file_type = graphene.String()

    def resolve_likes_count(self, info):
        return self.likes.all().count()

    def resolve_comments_count(self, info):
        return self.comments.all().count()

    def resolve_likes(self, info):
        return self.likes.all()

    def resolve_comments(self, info):
        return self.comments.all().order_by("-created_date")

    def resolve_file_type(self, info):
        if self.file:
            file_type, t = mimetypes.guess_type(str(self.file))
            return file_type.split("/")[0]
        return "unknown"


class MultiStoryType(graphene.ObjectType):
    user = graphene.Field(UserTypeone)
    stories = DjangoFilterConnectionField(StoryType)
    batch_number = graphene.Int()


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ("id", "user", "momemt", 'created_at')


class CommentLikeType(DjangoObjectType):
    class Meta:
        model = CommentLike
        fields = "__all__"


class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        fields = ("id", "user", "momemt", "Report_msg")


class CommentReportType(DjangoObjectType):
    pk = graphene.Int(source="pk")
    class Meta:
        model = ReportComment
        fields = ("id", "user", "comment", "Report_msg", "timestamp")


class StoryReportType(DjangoObjectType):
    class Meta:
        model = StoryReport
        fields = "__all__"


class MomentsUpdateResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()


class UpdateMomentMutation(graphene.Mutation):
    Output = MomentsUpdateResponse

    class Arguments:
        pk = graphene.Int(required=True)
        moment_description = graphene.String(required=True)

    def mutate(self, info, pk, moment_description):
        muser = info.context.user
        try:
            moment = Moment.objects.get(pk=pk, user=muser)
            print(moment)
            moment.moment_description = modify_text(moment_description)
            moment.save()
            NotifyUpdateMoment.broadcast(payload=moment, group="moments")
            return MomentsUpdateResponse(
                success=True, message="Moment Updated Successfuly!"
            )
        except:
            return MomentsUpdateResponse(success=False, message="Moment not found!")


class Momentmutation(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        Title = graphene.String(required=True)
        moment_description = graphene.String(required=True)
        file = Upload(required=False)
        moderator_id = graphene.String(required=False)
        allow_comment = graphene.Boolean(required=False, default_value=True)
        stock_image_id = graphene.Int(required=False)
        # moment_description=graphene.String(required=True)

    moment = graphene.Field(MomentsTyps)

    @classmethod
    def mutate(
        cls, root, info, Title, moment_description,user,
            file=None,
            allow_comment=None,
            moderator_id=None,
            stock_image_id=None
    ):

        muser = info.context.user

        if (
            moderator_id
        ):  # if request sent my moderator then set user to moderator user.
            roles = [r.role for r in muser.roles.all()]
            if "ADMIN" in roles or "CHATTER" in roles or "REGULAR" in roles:
                # if not muser.fake_users.filter(id=moderator_id).exists():
                #     raise Exception("Invalid moderator id")
                muser = User.objects.filter(id=moderator_id).first()
            else:
                return Exception(translate_error_message(info.context.user, "User cannot create moderator story"))

        check_permission(
            user=muser,
            permission="SHARE_MOMENT",
            date_field="created_date",
            qs=Moment.objects.filter(user=muser),
        )

        icon = None
        avatar_url = None
        try:
            avatar_url = muser.avatar().file.url
        except:
            avatar_url = None

        if avatar_url:
            icon = info.context.build_absolute_uri(avatar_url)

        if stock_image_id:
            try:
                file = StockImage.objects.get(id=stock_image_id).file
            except:
                return Exception(translate_error_message(info.context.user, "Invalid stock Image Id"))

        new_moment = Moment(
            user=muser,
            Title=Title,
            moment_description=modify_text(moment_description),
            file=file,
            allow_comment=allow_comment
        )
        new_moment.save()
        status = None
        if not stock_image_id:
            status = detect_moment(new_moment, file)
        if status:
            return Exception(translate_error_message(info.context.user, "Your Moment has been submitted for admin review."))

        """Send notification to the followed User about the Moment that Logged-In user shared"""
        user_followers = ProfileFollow.objects.filter(following=muser)
        #Todo: below code need to be optimized
        if user_followers.exists():
            for user_follower in user_followers:
                notification_setting = "MMSHARED"
                try:
                    moderator = ChatsQue.objects.filter(worker=muser, isAssigned=True).first().moderator
                except:
                    return muser
                data = {
                    "momentId": new_moment.id,
                    "notification_type": notification_setting,
                }
                priority = None
                app_url = None
                android_channel_id = None
                notification_obj = Notification(
                    user=user_follower.follower,
                    sender=moderator,
                    app_url=app_url,
                    notification_setting_id=notification_setting,
                    data=data,
                    priority=priority,
                )
                send_notification_fcm(
                    notification_obj=notification_obj,
                    android_channel_id=android_channel_id,
                    icon=icon,
                    image=icon
                )
        # send_moment_broadcast_fcm(moment_obj=new_moment, icon=icon, image=icon)
        NotifyNewMoment.broadcast(payload=new_moment, group="moments")
        return Momentmutation(moment=new_moment)


class NotifyMoment(channels_graphql_ws.Subscription):
    moment = graphene.Field(MomentsTyps)
    liked_by_users_list = graphene.List(UserTypeone)
    id = graphene.ID()

    class Arguments:
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, token, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login = datetime.datetime.now()
            user.save()
            if user.fake_users.all().count() > 0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception(translate_error_message(info.context.user, "Invalid moderator_id"))
                    user = User.objects.get(id=moderator_id)
                    user.last_login = datetime.datetime.now()
                    user.save()
                # else:
                #     raise Exception("moderator_id required")

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return ["moments"]

    @staticmethod
    def publish(payload, info, token=None, moderator_id=None):
        user_ids = payload.momemt_for_like.all().values_list("user", flat=True)
        liked_by_users_list = User.objects.filter(id__in=user_ids)
        return NotifyNewMoment(moment=payload, liked_by_users_list=liked_by_users_list)


class NotifyNewMoment(NotifyMoment):
    pass


class NotifyUpdateMoment(NotifyMoment):
    pass


class NotifyDeleteComment(channels_graphql_ws.Subscription):
    comment = graphene.JSONString()
    id = graphene.ID()

    class Arguments:
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, token, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login = datetime.datetime.now()
            user.save()
            if user.fake_users.all().count() > 0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception(translate_error_message(info.context.user, "Invalid moderator_id"))
                    user = User.objects.get(id=moderator_id)
                    user.last_login = datetime.datetime.now()
                    user.save()
                else:
                    raise Exception(translate_error_message(info.context.user, "moderator_id required"))

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return ["comments"]

    @staticmethod
    def publish(payload, info, token=None, moderator_id=None):
        return NotifyDeleteComment(comment=payload, id=payload["id"])


class NotifyDeleteMoment(channels_graphql_ws.Subscription):
    moment = graphene.JSONString()
    id = graphene.ID()

    class Arguments:
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, token, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login = datetime.datetime.now()
            user.save()
            if user.fake_users.all().count() > 0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception(translate_error_message(info.context.user, "Invalid moderator_id"))
                    user = User.objects.get(id=moderator_id)
                    user.last_login = datetime.datetime.now()
                    user.save()
                else:
                    raise Exception(translate_error_message(info.context.user, "moderator_id required"))

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return ["moments"]

    @staticmethod
    def publish(payload, info, token=None, moderator_id=None):
        return NotifyDeleteMoment(moment=payload, id=payload["id"])


class OnUpdateStory(channels_graphql_ws.Subscription):
    """Subscription triggers on new like and comment occurs."""

    story_id = graphene.Int()
    likes_count = graphene.Int()
    comments_count = graphene.Int()
    likes = DjangoFilterConnectionField(GenericLikeType)
    comments = DjangoFilterConnectionField(GenericCommentType)
    liked_by_users_list = graphene.List(UserTypeone)

    class Arguments:
        stories_list = graphene.List(graphene.NonNull(graphene.Int))

    def subscribe(cls, info, stories_list):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info, stories_list=[]):
        print(stories_list)
        story = Story.objects.filter(id=self["story_id"]).first()
        if story:
            likes = story.likes.all()
            comments = story.comments.all()
            user_ids = likes.values_list("user", flat=True)
            liked_by_users_list = User.objects.filter(id__in=user_ids)
            return OnUpdateStory(
                story_id=story.id,
                likes_count=likes.count(),
                comments_count=comments.count(),
                likes=likes,
                comments=comments.order_by("-created_date"),
                liked_by_users_list=liked_by_users_list,
            )


class OnDeleteStory(channels_graphql_ws.Subscription):
    """Subscription triggers on a delete story occurs."""

    user_id = graphene.String()
    story_id = graphene.Int()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        return OnDeleteStory(
            user_id=self["user_id"],
            story_id=self["story_id"],
        )


class OnNewStory(channels_graphql_ws.Subscription):
    """Subscription triggers on a new story occurs."""

    user = graphene.Field(UserTypeone)
    stories = DjangoFilterConnectionField(StoryType)
    batch_number = graphene.Int()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        limit = UserLimit.objects.get(action_name="MultiStoryLimit").limit_value
        total_stories = Story.objects.filter(
            user__id=self["user_id"],
            created_date__gte=datetime.datetime.now() - datetime.timedelta(hours=24),
        ).order_by("-created_date")
        batch_number = total_stories.count() / limit
        batch_number = batch_number if batch_number.is_integer() else batch_number + 1
        stories_to_send = total_stories.count() % limit
        if stories_to_send:
            results = {
                "user": User.objects.get(id=self["user_id"]),
                "stories": total_stories[:stories_to_send],
                "batch_number": batch_number,
            }
        else:
            results = {
                "user": User.objects.get(id=self["user_id"]),
                "stories": total_stories[:limit],
                "batch_number": batch_number,
            }
        return OnNewStory(
            user=results["user"],
            stories=Story.objects.filter(id__in=[i.id for i in results["stories"]]),
            batch_number=results["batch_number"],
        )


# def createThumbnail(**kwargs):
#     file=kwargs['file']
#     story=kwargs['story']
#     print(file)
#     print(story)
#     with tempfile.NamedTemporaryFile(mode="wb") as vid:


#                 vidcap = cv2.VideoCapture(story.file.path)

#                 success,image = vidcap.read()

#                 if success:
#                     _, img = cv2.imencode('.jpeg', image)
#                     img.tobytes()
#                     file = ContentFile(img)
#                     story.thumbnail.save('thumbnail.jpeg', file , save=True)
#                     return


class Storymutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=False)
        moderator_id = graphene.String(required=False)
        stock_image_id = graphene.Int(required=False)

    story = graphene.Field(StoryType)

    @classmethod
    def mutate(cls, root, info, file=None, moderator_id=None, stock_image_id=None):
        user = info.context.user
        if (
            moderator_id
        ):  # if request sent my moderator then set user to moderator user.
            roles = [r.role for r in user.roles.all()]
            if "ADMIN" in roles or "CHATTER" in roles or "REGULAR" in roles:
                # if not user.fake_users.filter(id=moderator_id).exists():
                #     raise Exception("Invalid moderator id")
                user = User.objects.filter(id=moderator_id).first()
            else:
                return Exception(translate_error_message(info.context.user, "User cannot create moderator story"))

        check_permission(
            user=user,
            permission="SHARE_STORY",
            date_field="created_date",
            qs=Story.objects.filter(user=user),
        )

        if stock_image_id:
            try:
                file = StockImage.objects.get(id=stock_image_id).file
            except:
                return Exception(translate_error_message(info.context.user, "Invalid stock Image Id"))

        new_story = Story(user=user, file=file)
        file_type, t = mimetypes.guess_type(str(file))
        if file_type.split("/")[0] == "video":
            try:
                with open("static/img/thumbnail.png", "rb") as f:
                    thumbnail = File(f)
                    new_story.thumbnail.save("thumbnail.jpeg", thumbnail, save=True)
            except FileNotFoundError:
                raise Exception(translate_error_message(info.context.user, "Thumbnail image does not exist"))
            createThumbnail.delay(new_story.id)

        new_story.save()
        status = None
        if not stock_image_id:
            status = detect_story(new_story, file)  # if nude
        if status:
            return Exception(translate_error_message(info.context.user, "Your Story has been submitted for admin review."))

        """Send notification to the followed User about the Story that Logged-In user shared"""
        user_followers = ProfileFollow.objects.filter(following=user)
        icon = None
        avatar_url = None
        try:
            avatar_url = user.avatar().file.url
        except:
            avatar_url = None

        if avatar_url:
            icon = info.context.build_absolute_uri(avatar_url)
        # Todo: below code need to be optimized
        if user_followers.exists():
            for user_follower in user_followers:
                notification_setting = "STSHARED"
                try:
                    moderator = ChatsQue.objects.filter(worker=user, isAssigned=True).first().moderator
                except:
                    return user
                data = {
                    "storyId": new_story.id,
                    "notification_type": notification_setting,
                }
                priority = None
                app_url = None
                android_channel_id = None
                notification_obj = Notification(
                    user=user_follower.follower,
                    sender=moderator,
                    app_url=app_url,
                    notification_setting_id=notification_setting,
                    data=data,
                    priority=priority,
                )
                send_notification_fcm(
                    notification_obj=notification_obj,
                    android_channel_id=android_channel_id,
                    icon=icon,
                    image=icon
                )

        OnNewStory.broadcast(
            group=None,
            payload={"user_id": str(new_story.user.id), "story_id": new_story.id},
        )
        return Storymutation(story=new_story)


class DeleteMomentType(graphene.ObjectType):
    id = graphene.Int()


class MomentDeleteMutation(graphene.Mutation):

    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            delete_moment = Moment.objects.filter(id=id).first()
            delete_moment.delete()

            NotifyDeleteMoment.broadcast(payload={"id": id}, group="moments")
            return MomentDeleteMutation(success=translate_error_message(info.context.user, "delete successfully"), id=id)

        except Exception as e:
            print(e, traceback.print_exc())
            raise Exception(translate_error_message(info.context.user, "invalid moment id"))


class Storydeletemutation(graphene.Mutation):
    success = graphene.String()
    id = graphene.Int()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        # print(request.user)
        user = info.context.user

        try:
            if user.roles.filter(role__in=["ADMIN"]):
                delete_story = Story.objects.filter(id=id).first()
            else:
                delete_story = Story.objects.filter(id=id, user=user).first()

            story_id = delete_story.id
            delete_story.delete()

            OnDeleteStory.broadcast(
                group=None, payload={"user_id": str(user.id), "story_id": story_id}
            )
            return Storydeletemutation(
                success=translate_error_message(info.context.user, "Story deleted successfully"), id=story_id
            )
        except:
            raise Exception(translate_error_message(info.context.user, "invalid story id or not have access to delete"))


class Momentlikemutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id = graphene.ID()
        moderator_id = graphene.UUID(required=False)

    like = graphene.Field(LikeType)

    @classmethod
    def mutate(cls, root, info, moment_id, moderator_id=None):

        user = get_worker_user(info.context.user, moderator_id)

        try:
            moment = Moment.objects.get(id=moment_id)
        except Moment.DoesNotExist:
            return Exception(translate_error_message(info.context.user, "Invalid moment_id"))

        like = Like.objects.filter(user=user, momemt_id=moment_id)
        if like.exists():
            like = like[0]
            like.delete()
            NotifyUpdateMoment.broadcast(payload=moment, group="moments")
            return Momentlikemutation(like=like)
        new_like = Like(user=user, momemt_id=moment_id)
        new_like.save()
        # new_like.save()
        # TODO: set data payload, user avtar as icon
        notification_setting = "LIKE"
        try:
            moderator = ChatsQue.objects.filter(worker=user, isAssigned=True).first().moderator
        except:
            return user
        data = {
            "momentId": moment.id,
            "likeID": new_like.id,
            "notification_type": notification_setting,
        }
        priority = None
        icon = None
        app_url = None
        android_channel_id = None

        notification_obj = Notification(
            user=moment.user,
            sender=moderator,
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

        """Send notification to the followed User about Logged In user liked a Moment"""
        user_followers = ProfileFollow.objects.filter(following=user).values_list('follower', flat=True)
        if user_followers:
            notifications = [
                Notification(
                    user=user_follower,
                    sender=user,
                    app_url=app_url,
                    notification_setting_id=notification_setting,
                    data=data,
                    priority=priority,
                ) for user_follower in user_followers
            ]
            send_notification_fcm(
                notification_obj=notifications,
                android_channel_id=android_channel_id,
                icon=icon,
            )

        NotifyUpdateMoment.broadcast(payload=moment, group="moments")

        return Momentlikemutation(like=new_like)


class CommentLikeMutation(graphene.Mutation):
    class Arguments:
        comment_id = graphene.String()

    comment_like = graphene.Field(CommentLikeType)

    @classmethod
    def mutate(cls, root, info, comment_id):
        user = info.context.user
        commentlike = CommentLike.objects.filter(user=user, comment_id=comment_id)
        if commentlike.exists():
            commentlike = commentlike[0]
            commentlike.delete()
            return CommentLikeMutation(commentlike)

        new_commentlike = CommentLike(user=user, comment_id=comment_id)
        new_commentlike.save()
        notification_to = new_commentlike.comment.user

        # TODO: set data payload, user avtar as icon
        data = {}
        priority = None
        icon = None
        app_url = None
        android_channel_id = None
        notification_setting = "CMNTLIKE"

        notification_obj = Notification(
            user=notification_to,
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
        )

        return CommentLikeMutation(new_commentlike)


class Momentcommentmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id = graphene.ID()
        comment_description = graphene.String(required=True)
        reply_to = graphene.String(required=False)
        moderator_id = graphene.UUID(required=False)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, moment_id, comment_description, reply_to=None, moderator_id=None):

        user = get_worker_user(info.context.user, moderator_id)

        try:
            moment = Moment.objects.get(id=moment_id)
        except Moment.DoesNotExist:
            return Exception(translate_error_message(info.context.user, "Invalid moment_id"))

        if not moment.allow_comment:
            return Exception(translate_error_message(info.context.user, "Comments has been blocked by the user for this post!"))

        comment_description = modify_text(comment_description)
        new_comment = Comment(
            user=user,
            momemt_id=moment_id,
            comment_description=comment_description,
            reply_to_id=reply_to,
        )
        new_comment.save()

        notification_to = new_comment.momemt.user

        # TODO: set data payload, user avtar as icon
        notification_setting = "CMNT"
        try:
            moderator = ChatsQue.objects.filter(worker=user, isAssigned=True).first().moderator
        except:
            return user
        data = {
            "momentId": int(moment_id),
            "commentID": new_comment.id,
            "notification_type": notification_setting,
        }
        priority = None
        icon = None
        app_url = None
        android_channel_id = None

        # notification_obj = Notification(
        #     user=notification_to,
        #     sender=user,
        #     app_url=app_url,
        #     notification_setting_id=notification_setting,
        #     data=data,
        #     priority=priority,
        # )
        # send_notification_fcm(
        #     notification_obj=notification_obj,
        #     android_channel_id=android_channel_id,
        #     icon=icon,
        # )
        """Send notification to the followed User about Logged In user Comment a Moment"""
        user_followers = ProfileFollow.objects.filter(following=user)
        # Todo: below code need to be optimized
        if user_followers.exists():
            for user_follower in user_followers:
                notification_obj = Notification(
                    user=user_follower.follower,
                    sender=moderator,
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

        NotifyUpdateMoment.broadcast(payload=moment, group="moments")

        return Momentcommentmutation(comment=new_comment)


class Momentreportmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id = graphene.ID()
        Report_msg = graphene.String(required=True)

    report = graphene.Field(ReportType)

    @classmethod
    def mutate(cls, root, info, moment_id, Report_msg):
        user = info.context.user
        moment = None
        try:
            moment = Moment.objects.get(id=moment_id)
        except Moment.DoesNotExist:
            raise Exception(translate_error_message(info.context.user, "Moment does not exist"))
        if moment.user == user:
            raise Exception(translate_error_message(info.context.user, "You cannot report your moments"))
        new_report = Report(user=user, momemt_id=moment_id, Report_msg=Report_msg)
        new_report.save()
        return Momentreportmutation(report=new_report)


class Storyreportmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        story_id = graphene.ID()
        Report_msg = graphene.String(required=True)

    story_report = graphene.Field(StoryReportType)

    @classmethod
    def mutate(cls, root, info, story_id, Report_msg):
        user = info.context.user
        story = None
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            raise Exception(translate_error_message(info.context.user, "Story does not exist"))
        if story.user == user:
            raise Exception(translate_error_message(info.context.user, "You cannot report your story"))
        new_report = StoryReport(user=user, story_id=story_id, Report_msg=Report_msg)
        new_report.save()
        return Storyreportmutation(story_report=new_report)


class TranslateMomentMutation(graphene.Mutation):
    class Arguments:
        moment_id = graphene.Int()

    translated_text = graphene.String()

    @classmethod
    def mutate(cls, root, info, moment_id):
        moment = Moment.objects.get(id=moment_id)

        return TranslateMomentMutation(
            translated_text=custom_translate(
                info.context.user, moment.moment_description
            )
        )


class GenericCommentMutation(graphene.Mutation):
    generic_comment = graphene.Field(GenericCommentType)

    class Arguments:
        object_type = graphene.String()
        comment_description = graphene.String()
        object_id = graphene.Int()
        moderator_id = graphene.UUID(required=False)

    @classmethod
    def mutate(cls, root, info, object_type, object_id, comment_description, moderator_id=None):
        user = get_worker_user(info.context.user, moderator_id)
        content_type = ContentType.objects.get(app_label="moments", model=object_type)
        comment_description = modify_text(comment_description)
        new_comment = GenericComment(
            user=user,
            comment_description=comment_description,
            content_type=content_type,
            object_id=object_id,
        )
        new_comment.save()

        story_id = object_id
        if object_type == "genericcomment":
            parent_comment = GenericComment.objects.get(id=object_id)
            story_id = parent_comment.object_id

        story = Story.objects.get(id=story_id)

        OnUpdateStory.broadcast(group=None, payload={"story_id": story.id})

        notification_to = story.user
        # TODO: set data payload, user avtar as icon

        notification_setting = "STCMNT"
        try:
            moderator = ChatsQue.objects.filter(worker=user, isAssigned=True).first().moderator
        except:
            return user
        data = {
            "comment_comment_description": comment_description,
            "storyID": story.id,
            "commentID": new_comment.id,
            "notification_type": notification_setting,
            "comment_description": comment_description,
        }
        priority = None
        icon = None
        app_url = None
        android_channel_id = None

        notification_obj = Notification(
            user=notification_to,
            sender=moderator,
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

        return GenericCommentMutation(new_comment)


class GenericLikeMutation(graphene.Mutation):
    generic_like = graphene.Field(GenericLikeType)

    class Arguments:
        object_type = graphene.String()
        object_id = graphene.Int()
        moderator_id = graphene.UUID(required=False)

    @classmethod
    def mutate(cls, root, info, object_type, object_id, moderator_id=None):
        user = get_worker_user(info.context.user, moderator_id)
        content_type = ContentType.objects.get(app_label="moments", model=object_type)
        like = GenericLike.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        )
        if like.exists():
            like = like[0]
            like.delete()
            return GenericLikeMutation(like)
        new_like = GenericLike(
            user=user, content_type=content_type, object_id=object_id
        )
        new_like.save()

        story_id = object_id
        if object_type == "genericcomment":
            generic_comment = GenericComment.objects.get(id=object_id)
            if generic_comment.content_type == content_type:
                generic_comment = GenericComment.objects.get(
                    id=generic_comment.object_id
                )
            story_id = generic_comment.object_id

        story = Story.objects.get(id=story_id)

        OnUpdateStory.broadcast(group=None, payload={"story_id": story.id})

        notification_to = story.user
        # TODO: set data payload, user avtar as icon
        notification_setting = "STLIKE"
        try:
            moderator = ChatsQue.objects.filter(worker=user, isAssigned=True).first().moderator
        except:
            return user
        data = {
            "pk": story.id,
            "storyID": story.id,
            "likeID": new_like.id,
            "notification_type": notification_setting,
        }
        priority = None
        icon = None
        app_url = None
        android_channel_id = None

        notification_obj = Notification(
            user=notification_to,
            sender=moderator,
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
        return GenericLikeMutation(new_like)


class CommentDeleteMutation(graphene.Mutation):
    """Mutation for Deleting a Comment"""
    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user
        try:
            comment_obj = Comment.objects.get(id=id)

        except Exception as e:
            print(e, traceback.print_exc())
            raise Exception(translate_error_message(info.context.user, "invalid comment id"))

        if not Comment.objects.filter(id=id, momemt__user=user).exists():
            raise Exception(translate_error_message(info.context.user, "User can only delete the comments posted on his/her Moment"))
        comment_obj.delete()
        NotifyDeleteComment.broadcast(payload={"id": id}, group="comments")
        return MomentDeleteMutation(success=translate_error_message(info.context.user, "delete successfully"), id=id)


class Commentreportmutation(graphene.Mutation):
    comment_report = graphene.Field(CommentReportType)
    report_count = graphene.Int()

    class Arguments:
        comment_id = graphene.Int()
        Report_msg = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, comment_id, Report_msg):
        user = info.context.user
        comment = None
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise Exception(translate_error_message(info.context.user, "Comment does not exist"))
        if comment.user == user:
            raise Exception(translate_error_message(info.context.user, "You cannot report your comments"))
        if ReportComment.objects.filter(user=user, comment_id=comment_id).exists():
            raise Exception(translate_error_message(info.context.user, "You had already reported this comment!"))
        new_report = ReportComment(user=user, comment_id=comment_id, Report_msg=Report_msg)
        new_report.save()        
        report_count = ReportComment.objects.filter(comment=comment_id).count()
        return Commentreportmutation(comment_report=new_report, report_count=report_count)

class Mutation(graphene.ObjectType):
    insert_moment = Momentmutation.Field()
    insert_story = Storymutation.Field()
    delete_moment = MomentDeleteMutation.Field()
    delete_story = Storydeletemutation.Field()
    update_moment = UpdateMomentMutation.Field()
    like_moment = Momentlikemutation.Field()
    comment_moment = Momentcommentmutation.Field()
    delete_comment = CommentDeleteMutation.Field()
    report_moment = Momentreportmutation.Field()
    report_story = Storyreportmutation.Field()
    like_comment = CommentLikeMutation.Field()
    report_comment = Commentreportmutation.Field()
    generic_comment = GenericCommentMutation.Field()
    generic_like = GenericLikeMutation.Field()
    translate_moment = TranslateMomentMutation.Field()


class Query(graphene.ObjectType):

    # all_user_stories=DjangoFilterConnectionField(StoryType)
    # all_user_moments = DjangoFilterConnectionField(MomentsTyps)
    # all_user_comments = DjangoFilterConnectionField(CommentType)

    # def resolve_all_user_stories(root, info):
    #     return Story.objects.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=EXPIRE_TIME)).order_by('-created_date','user')

    current_user_moments = graphene.List(MomentsTyps)
    all_moments = graphene.List(MomentsTyps)
    current_user_stories = graphene.List(StoryType)
    all_user_stories = DjangoFilterConnectionField(StoryType)
    all_user_multi_stories = graphene.List(MultiStoryType)
    all_comments = graphene.List(CommentType, moment_id=graphene.String(required=True))
    all_comment_reports = graphene.List(CommentReportType, comment_id=graphene.Int(required=True))
    get_moment_likes = graphene.List(LikeType, moment_pk=graphene.Int(required=True))
    get_moment_comments = graphene.List(CommentType, moment_pk=graphene.Int(required=True))
    all_user_moments = DjangoFilterConnectionField(MomentsTyps)
    all_user_comments = DjangoFilterConnectionField(CommentType)
    user_stories = graphene.List(UserStories, user_id=graphene.ID(required=True))

    def resolve_all_user_moments(self, info, **kwargs):
        user = info.context.user
        return Moment.objects.exclude(
            user__blockedUsers__username=user.username
        ).order_by("-created_date")

    def resolve_all_user_stories(self, info, **kwargs):
        user = info.context.user
        return Story.objects.order_by("-created_date")

    def resolve_all_user_multi_stories(self, info, **kwargs):
        return all_user_multi_stories_query(info)

    def resolve_all_comments(self, info, **kwargs):
        momentId = kwargs.get("moment_id")
        return Comment.objects.filter(momemt_id=momentId, reply_to=None).order_by(
            "-created_date"
        )

    def resolve_all_comment_reports(self, info, **kwargs):
        comment_id = kwargs.get("comment_id")
        return ReportComment.objects.filter(comment=comment_id).order_by("-timestamp")

    def resolve_get_moment_likes(self, info, **kwargs):
        # user = info.context.user
        momentPk = kwargs.get("moment_pk")
        # print('moment id = ',momentId)
        # print(Like.objects.filter(momemt__pk=momentId))
        return Like.objects.filter(momemt__pk=momentPk).order_by("-id")

    def resolve_get_moment_comments(self, info, **kwargs):
        # user = info.context.user
        momentPk = kwargs.get("moment_pk")
        # print('moment id = ',momentId)
        # print(Like.objects.filter(momemt__pk=momentId))
        return Comment.objects.filter(momemt__pk=momentPk).order_by("-id")

    def resolve_all_moments(self, info):
        return Moment.objects.all().order_by("-created_date")

    # def resolve_all_user_stories(root, info):
    #     return Story.objects.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=EXPIRE_TIME)).order_by('-created_date','user')

    def resolve_current_user_stories(root, info):

        user = info.context.user
        return Story.objects.filter(
            user=user,
            created_date__gte=datetime.datetime.now()
            - datetime.timedelta(seconds=EXPIRE_TIME),
        ).order_by("-created_date")

    def resolve_current_user_moments(root, info):

        user = info.context.user
        return Moment.objects.filter(user=user).all().order_by("-created_date")

    def resolve_user_stories(self, info, **kwargs):
        user_id = kwargs.get("user_id")
        user_stories = Story.objects.filter(user__id=user_id)
        if user_stories:
            return user_stories
        else:
            return None
    def resolve_all_comment_reports(self, info, **kwargs):
        comment_id = kwargs.get("comment_id")
        return ReportComment.objects.filter(comment_id=comment_id).all().order_by("-timestamp")


class Subscription(graphene.ObjectType):
    on_new_story = OnNewStory.Field()
    on_delete_story = OnDeleteStory.Field()
    on_update_story = OnUpdateStory.Field()
    on_new_moment = NotifyNewMoment.Field()
    on_update_moment = NotifyUpdateMoment.Field()
    on_delete_moment = NotifyDeleteMoment.Field()
    on_delete_comment = NotifyDeleteComment.Field()
