from itertools import chain
import graphene
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from graphene_django import DjangoObjectType
import geopy.distance
from django.contrib.auth import get_user_model
from graphene.utils.resolve_only_args import resolve_only_args
import payments
from reports.models import Reported_Users
import user.schema
import channels_graphql_ws
from googletrans import Translator

translator = Translator()

from subscriptions.models import ModeratorSubscriptionPlan
from user.models import (
    User,
    UserSocialProfile,
    PrivatePhotoViewRequest,
    PrivatePhotoViewTime,
    Settings,
    CoinSettings,
    CoinSettingsForRegion,
    ProfileFollow,
    ProfileVisit,
    FeatureSettings,
    CoinSpendingHistory,
    UserProfileTranlations,
    ChatsQue,
    UserRole
)
from defaultPicker.models import (
    tags,
    music as Music,
    movies as Movies,
    sportsTeams as SportsTeams,
    tvShows as TVShow,
    book as Book,
    height as Height,
    age as Age,
    Language,
)
import reports.schema
import purchase.schema
import payments.schema
import defaultPicker.schema
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
import chat.schema
from django.db.models import Count, F
from user.schema import UserPhotoType, ProfileVisitSubscription, OnUserOnline
from graphql.error import GraphQLError
import gifts.schema
import moments.schema
import stock_image.schema
from gifts.models import Giftpurchase
from push_notifications.models import GCMDevice

# from graphql_auth import mutations
from user.utils import get_country_from_geo_point, translate_error_message, get_zipcode
import channels
from chat.models import Notification, send_notification_fcm
from moments.utils import modify_text
from user.tasks import send_notification_to_nearby_users
from purchase.models import PackagePurchase, Permission, Package
from defaultPicker.utils import translated_field_name


userroles = UserRole.objects.filter(role=UserRole.ROLE_FAKE_USER).exists()
if userroles:
    MODERATOR_ID = UserRole.objects.get(role=UserRole.ROLE_FAKE_USER).id
else:
    MODERATOR_ID = 1



class AuthMutation(graphene.ObjectType):
    pass
    # register = mutations.Register.Field()
    # verify_account = mutations.VerifyAccount.Field()
    # resend_activation_email = mutations.ResendActivationEmail.Field()
    # send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    # password_reset = mutations.PasswordReset.Field()
    # password_set = mutations.PasswordSet.Field()  # For passwordless registration
    # password_change = mutations.PasswordChange.Field()
    # update_account = mutations.UpdateAccount.Field()
    # archive_account = mutations.ArchiveAccount.Field()
    # delete_account = mutations.DeleteAccount.Field()
    # send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    # verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    # swap_emails = mutations.SwapEmails.Field()
    # remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    # token_auth = mutations.ObtainJSONWebToken.Field()
    # verify_token = mutations.VerifyToken.Field()
    # refresh_token = mutations.RefreshToken.Field()
    # revoke_token = mutations.RevokeToken.Field()


class TagResponse(graphene.ObjectType):
    id = graphene.Int()
    tag = graphene.String()
    tag_fr = graphene.String()


class AvatarPhotoMixin:
    avatar_photos = graphene.List(UserPhotoType)

    def resolve_avatar_photos(self, info):
        return self.avatar_photos.all()


class likedUsersResponse(graphene.ObjectType, AvatarPhotoMixin):
    id = graphene.String()
    username = graphene.String()
    full_name = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)

    def resolve_full_name(self, info):
        return self.fullName

    def resolve_id(self, info):
        return self.id

    def resolve_username(self, info):
        return self.username

    # depricated
    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))


class blockedUsersResponse(graphene.ObjectType, AvatarPhotoMixin):
    id = graphene.String()
    username = graphene.String()
    full_name = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)

    def resolve_full_name(self, info):
        return self.fullName

    def resolve_id(self, info):
        return self.id

    def resolve_username(self, info):
        return self.username

    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))


class InResponse(graphene.ObjectType):
    id = graphene.Int()
    interest = graphene.String()
    interest_fr = graphene.String()


class attrTranslationType(graphene.ObjectType):
    name = graphene.String()
    name_translated = graphene.String()


class UserAttrTranslationType(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = UserProfileTranlations
        fields = "__all__"

    def resolve_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "name"))


class UserFollowType(DjangoObjectType, AvatarPhotoMixin):
    is_connected = graphene.Boolean()
    datetime = graphene.DateTime()
    datetime_visiting = graphene.DateTime()
    followers_count = graphene.Int()
    following_count = graphene.Int()

    class Meta:
        model = User
        fields = "__all__"

    def resolve_is_connected(self, info):
        requested_user = info.context.user
        user = get_user_model().objects.get(id=self.id)
        if requested_user == user:
            return None
        return ProfileFollow.objects.filter(follower=requested_user, following_id=self.id).exists()

    def resolve_datetime(self, info):
        try:
            latest_visitor = ProfileVisit.objects.filter(
                visitor_id=self.id).order_by("-created_at").first()
            return latest_visitor.created_at
        except:
            return None

    def resolve_datetime_visiting(self, info):
        try:
            latest_visited = ProfileVisit.objects.filter(
                visiting_id=self.id).order_by("-created_at").first()
            return latest_visited.created_at
        except:
            return None

    def resolve_followers_count(self, info):
        return ProfileFollow.objects.filter(following_id=self.id).count()

    def resolve_following_count(self, info):
        return ProfileFollow.objects.filter(follower_id=self.id).count()


from moments.models import User, Story, StoryReport
from moments.schema import ReportType
class StoryReportType1(DjangoObjectType):
    class Meta:
        model = StoryReport


class StoryType1(DjangoObjectType):
    class Meta:
        model = Story

    story_reports = graphene.List(StoryReportType1)

    def resolve_story_reports(self, info):
        return self.story_for_report.all()

class UserType(DjangoObjectType, AvatarPhotoMixin):
    class Meta:
        model = User
        fields = ("avatar_index",)

    id = graphene.String()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    gender = graphene.Int()
    about = graphene.String()
    location = graphene.List(graphene.Float)
    isOnline = graphene.Boolean()
    familyPlans = graphene.Int()
    age = graphene.Int()
    language = graphene.List(graphene.Int)
    language_id_code = graphene.String()
    user_language_code = graphene.String()
    address = graphene.String()
    tags = graphene.List(graphene.Int)
    politics = graphene.Int()
    purchase_coins = graphene.Int()
    gift_coins = graphene.Int()
    coins = graphene.Int()
    zodiacSign = graphene.Int()
    height = graphene.Int()
    photos_quota = graphene.Int()
    interested_in = graphene.List(graphene.Int)
    ethinicity = graphene.Int()
    religion = graphene.Int()
    blocked_users = graphene.List(blockedUsersResponse)
    education = graphene.String()
    music = graphene.List(graphene.String)
    tvShows = graphene.List(graphene.String)
    sportsTeams = graphene.List(graphene.String)
    movies = graphene.List(graphene.String)
    work = graphene.String()
    books = graphene.List(graphene.String)
    avatar = graphene.Field(UserPhotoType)
    avatar_photos = graphene.List(UserPhotoType)
    likes = graphene.List(likedUsersResponse)
    last_seen = graphene.String()
    online = graphene.Boolean()
    received_gifts = graphene.List(gifts.schema.GiftpurchaseType)
    distance = graphene.String()
    private_photo_request_status = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    country_code = graphene.String()
    country_flag = graphene.String()
    followers_count = graphene.Int()
    following_count = graphene.Int()
    is_connected = graphene.Boolean()
    follower_users = graphene.List(UserFollowType)
    following_users = graphene.List(UserFollowType)
    user_visitors_count = graphene.Int()
    user_visiting_count = graphene.Int()
    user_visitors = graphene.List(UserFollowType)
    user_visiting = graphene.List(UserFollowType)
    user_subscription = graphene.Field(purchase.schema.UserSubscriptionType)
    user_attr_translation = graphene.List(UserAttrTranslationType)
    planname = graphene.String()
    is_moderator = graphene.Boolean()
    stories = graphene.List(StoryType1)
    momemts = graphene.List(ReportType)
    zip_code = graphene.String()
    # allow_manual_chat = graphene.Boolean()
    paste_access = graphene.Boolean()
    subscription = graphene.String()

    def resolve_is_moderator(self, info):
        return self.is_fake
    
    def resolve_stories(self, info):
        return self.story_set.all()

    def resolve_momemts(self, info):
        return self.User_for_report.all()

    def resolve_zip_code(self, info):
        return self.zip_code

    # def resolve_allow_manual_chat(self, info):
    #     return self.allow_manual_chat

    def resolve_paste_access(self, info):
        return self.paste_access

    def resolve_planname(self, info):
        try:
            # print(dir(user.profilevisit))
            # print(">>>>>>>>>>>>>>",self.id, user,PackagePurchase.objects.filter(user__id = self.id).values())
            package_id = PackagePurchase.objects.filter(user__id=self.id)[
                0].package_id
            # print(">>>>>>>>>>>>>>usser",)
            # print(graphene.Int(source= "pk"))
            # print(">>>>>>>>>>>", Package.objects.filter(id = package_id).values())
            planname_user = Package.objects.filter(id=package_id)[0].name
            return planname_user
        except:
            return "Not Active Plan"
    # depricated
    # photos = graphene.List(PhotoObj)

    def resolve_distance(self, info):
        return self.distance

    def resolve_avatar(self, info):
        return self.avatar()

    def resolve_received_gifts(self, info):
        return Giftpurchase.objects.filter(receiver_id=self.id)

    def resolve_username(self, info):
        return self.username

    def resolve_first_name(self, info):
        return self.first_name
    
    def resolve_last_name(self, info):
        return self.last_name

    def resolve_language_id_code(self, info):
        return self.get_language_id_code()

    def resolve_user_language_code(self, info):
        return self.user_language_code

    def resolve_address(self, info):
        return self.address

    def resolve_last_seen(self, info):
        return self.last_seen()

    def resolve_online(self, info):
        return self.online()

    def resolve_avatar_photos(self, info):
        return list(chain(self.avatar_photos.all(), self.private_avatar_photos.all()))

    def resolve_private_photo_request_status(self, info):
        if info.context.user == self:
            return ""
        else:
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=self,
                requested_user=info.context.user,
                updated_at__gte=datetime.now() - timedelta(hours=hours),
            ).first()

            if not request:
                return ""

            if request.status == "P":
                return "Cancel Request"
            else:
                return "Request Access"

    def resolve_coins(self, info):
        return self.purchase_coins

    def resolve_country_flag(self, info):
        if not self.country_code:
            return ""
        return info.context.build_absolute_uri(f"/static/img/country-flags/png250/{self.country_code}.png")

    @resolve_only_args
    def resolve_likes(self):
        user = get_user_model().objects.get(id=self.id)
        return user.likes.all()

    @resolve_only_args
    def resolve_age(self):
        user = get_user_model().objects.get(id=self.id)
        if user.age:
            return user.age.id
        return None

    @resolve_only_args
    def resolve_language(self):
        user = get_user_model().objects.get(id=self.id)
        if user.language.all().count() > 0:
            return list(user.language.all().values_list('id', flat=True))
        return None

    @resolve_only_args
    def resolve_height(self):
        user = get_user_model().objects.get(id=self.id)
        if user.height:
            return user.height.id
        return Height.objects.last().id

    @resolve_only_args
    def resolve_likes(self):
        user = get_user_model().objects.get(id=self.id)
        return user.likes.all()

    @resolve_only_args
    def resolve_tvShows(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.tvShows.values_list("interest", flat=True))

    @resolve_only_args
    def resolve_location(self):
        user = get_user_model().objects.get(id=self.id)
        if user.location:
            return list(map(float, user.location.split(",")))
        return []

    @resolve_only_args
    def resolve_books(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.book.values_list("interest", flat=True))

    @resolve_only_args
    def resolve_sportsTeams(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.sportsTeams.values_list("interest", flat=True))

    @resolve_only_args
    def resolve_movies(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.movies.values_list("interest", flat=True))

    @resolve_only_args
    def resolve_music(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.music.values_list("interest", flat=True))

    # depricated
    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))

    @resolve_only_args
    def resolve_tags(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.tags.values_list("id", flat=True))

    @resolve_only_args
    def resolve_interested_in(self):
        user = get_user_model().objects.get(id=self.id)
        return user.interestedIn_display

    @resolve_only_args
    def resolve_blocked_users(self):
        user = get_user_model().objects.get(id=self.id)
        return user.blockedUsers.all()

    def resolve_is_connected(self, info):
        requested_user = info.context.user
        user = get_user_model().objects.get(id=self.id)
        if requested_user == user:
            return None
        return ProfileFollow.objects.filter(follower=requested_user, following_id=self.id).exists()

    @resolve_only_args
    def resolve_followers_count(self):
        return ProfileFollow.objects.filter(following_id=self.id).count()

    @resolve_only_args
    def resolve_following_count(self):
        return ProfileFollow.objects.filter(follower_id=self.id).count()

    @resolve_only_args
    def resolve_user_visitors_count(self):
        return ProfileVisit.objects.filter(visiting_id=self.id).count()

    @resolve_only_args
    def resolve_user_visiting_count(self):
        return ProfileVisit.objects.filter(visitor_id=self.id).count()

    @resolve_only_args
    def resolve_follower_users(self):
        return User.objects.select_related().filter(user_follower__following__id=self.id)

    @resolve_only_args
    def resolve_following_users(self):
        return User.objects.select_related().filter(user_following__follower__id=self.id)

    @resolve_only_args
    def resolve_user_visitors(self):
        return User.objects.select_related().filter(user_visitor__visiting__id=self.id)

    @resolve_only_args
    def resolve_user_visiting(self):
        return User.objects.select_related().filter(user_visiting__visitor__id=self.id)

    @resolve_only_args
    def resolve_subscription(self):
        subscriptions = ModeratorSubscriptionPlan.objects.filter(moderator_id=self.id).last()
        if subscriptions:
            return subscriptions.subscription.name
        return None

    def resolve_user_subscription(self, info, **kwargs):
        user = info.context.user
        now = timezone.now()
        is_active = False
        subscription = PackagePurchase.objects.filter(
            user=user,
            is_active=True,
            starts_at__lte=now,
            ends_at__gte=now,
            renewed_at__isnull=True,
        ).first()
        if subscription:
            is_active = True

        return purchase.schema.UserSubscriptionType(
            is_active=is_active,
            package=subscription.package if subscription else None,
            plan=subscription.plan if subscription else None,
            starts_at=subscription.starts_at if subscription else None,
            ends_at=subscription.ends_at if subscription else None,
            cancelled_at=subscription.cancelled_at if subscription else None,
            is_cancelled=False
            if subscription and subscription.cancelled_at is None
            else True,
        )

    def resolve_user_attr_translation(self, info):
        return UserProfileTranlations.objects.order_by('created_at')




class userResponseObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)
    interested_in = graphene.List(graphene.Int)

    # depricated
    # @graphene.resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))

    @graphene.resolve_only_args
    def resolve_interested_in(self):
        return get_user_model().objects.get(id=self.id).interestedIn_display


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        # email = graphene.String(required=True)
        onesignal_player_id = graphene.String()
        fcm_registration_id = graphene.String()
        language = graphene.List(graphene.Int)

    def mutate(
        self,
        info,
        username,
        password,
        email,
        onesignal_player_id=None,
        fcm_registration_id=None,
        language=None
    ):
        user = get_user_model()(
            username=username, email=email, onesignal_player_id=onesignal_player_id
        )
        user.set_password(password)
        user.save()
        if language is not None:
            for language_id in language:
                languageObj = Language.objects.filter(id=language_id).first()
                if languageObj:
                    user.language.add(languageObj.id)

        if fcm_registration_id:
            GCMDevice.objects.get_or_create(
                registration_id=fcm_registration_id, cloud_message_type="FCM", user=user
            )
        return CreateUser(user=user)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        city = graphene.String()
        country = graphene.String()
        country_code = graphene.String()
        id = graphene.String()
        username = graphene.String()
        fullName = graphene.String()
        email = graphene.String()
        gender = graphene.Int()
        language = graphene.List(graphene.Int)
        user_language_code = graphene.String()
        about = graphene.String()
        location = graphene.List(graphene.Float)
        isOnline = graphene.Boolean()
        familyPlans = graphene.Int()
        age = graphene.Int()
        tag_ids = graphene.List(graphene.Int)
        politics = graphene.Int()
        zodiacSign = graphene.Int()
        height = graphene.Int()
        interested_in = graphene.List(graphene.Int)
        ethinicity = graphene.Int()
        religion = graphene.Int()
        education = graphene.String()
        music = graphene.List(graphene.String)
        tvShows = graphene.List(graphene.String)
        sportsTeams = graphene.List(graphene.String)
        movies = graphene.List(graphene.String)
        work = graphene.String()
        address = graphene.String()
        book = graphene.List(graphene.String)
        avatar_index = graphene.Int()
        onesignal_player_id = graphene.String()
        fcm_registration_id = graphene.String()
        # depricated
        # photos = graphene.List(graphene.String)
        likes = graphene.List(graphene.String)

        url = graphene.String()
        subscription_id = graphene.String()
        platform = graphene.Int(
            description="Number of social platform 1.GOOGLE 2.FACEBOOK 3.INSTAGRAM 4.SNAPCHAT 5.LINKEDIN"
        )
        paste_access = graphene.Boolean()
        # allow_manual_chat = graphene.Boolean()
        zip_code = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    Output = userResponseObj

    def mutate(
        self,
        info,
        id,
        username=None,
        fullName=None,
        language=None,
        user_language_code=None,
        gender=None,
        email=None,
        height=None,
        familyPlans=None,
        about=None,
        location=None,
        age=None,
        avatar_index=None,
        isOnline=None,
        tag_ids=None,
        url=None,
        platform=None,
        politics=None,
        zodiacSign=None,
        interested_in=None,
        ethinicity=None,
        religion=None,
        education=None,
        photos=None,
        onesignal_player_id=None,
        fcm_registration_id=None,
        music=None,
        likes=None,
        book=None,
        movies=None,
        sportsTeams=None,
        tvShows=None,
        work=None,
        address=None,
        subscription_id=None,
        paste_access=None,
        # allow_manual_chat=None,
        zip_code=None,
        first_name=None,
        last_name=None,
        country_code=None,
        city=None,
        country=None,
    ):
        global socialObj
        user = get_user_model().objects.get(id=id)
        try:
            profile = UserSocialProfile.objects.get(user=user)
        except:
            profile = None
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if country_code is not None:
            user.country_code = country_code
        if city is not None:
            user.city = city
        if country is not None:
            user.country = country
        if last_name is not None:
            user.last_name = last_name
        if fullName is not None:
            user.fullName = modify_text(fullName)
        if user_language_code is not None:
            user.user_language_code = user_language_code
        if gender is not None:
            user.gender = gender
        if language is not None:
            user.language.clear()
            for language_id in language:
                languageObj = Language.objects.filter(id=language_id).first()
                if languageObj:
                    user.language.add(languageObj.id)
        if subscription_id is not None:
            sub_obj = ModeratorSubscriptionPlan.objects.filter(moderator=user).first()
            if sub_obj is None:
                ModeratorSubscriptionPlan.objects.create(moderator=user, subscription_id=subscription_id)
            else:
                sub_obj.subscription_id = subscription_id
                sub_obj.save()
        if email is not None and email != "":
            user.email = email
        if height is not None:
            user.height_id = height
            heightObj = Height.objects.filter(height=height).first()
            if heightObj:
                user.height = heightObj.height
        if work is not None:
            user.work = work
        if address is not None:
            # if location:
            #     loc = list(map(str, location))
            #     user.location = f"{loc[0]}, {loc[1]}"
            #     zip_code = get_zipcode(loc[0], loc[1])
            #     if zip_code not in address:
            #         address = f"{address}-{zip_code}"
            #     user.zip_code = zip_code
            user.address = address
        if zip_code is not None:
            user.zip_code = zip_code
        if familyPlans is not None:
            user.familyPlans = familyPlans
        if about is not None:
            user.about = modify_text(about)
        if location is not None:
            loc = list(map(str, location))
            user.location = f"{loc[0]}, {loc[1]}"
            country, country_code, state, city, zip_code = get_country_from_geo_point(
                geo_point=location
            )
            user.country = country
            user.country_code = country_code
            user.state = state
            user.city = city
            # user.zip_code = zip_code

        if age is not None:
            # user.age_id = age
            ageObj = Age.objects.filter(id=age).first()
            if ageObj:
                user.age = ageObj
        if isOnline is not None:
            user.isOnline = isOnline
            if user.isOnline:
                # If user is online trigger the notification for the follower users
                OnUserOnline.notify_related_users(user)

        if tag_ids is not None:
            user.tags.clear()
            for tag_id in tag_ids:
                tag = tags.objects.get(id=tag_id)
                if tag is not None:
                    user.tags.add(tag)
        if politics is not None:
            user.politics = politics
        if music is not None:
            user.music.clear()
            for music_ in music:
                m, _ = Music.objects.get_or_create(
                    interest=music_, defaults={"interest": music_}
                )
                user.music.add(m)
        if movies is not None:
            user.movies.clear()
            for movie_ in movies:
                m, _ = Movies.objects.get_or_create(
                    interest=movie_, defaults={"interest": movie_}
                )
                user.movies.add(m)
        if sportsTeams is not None:
            user.sportsTeams.clear()
            for team in sportsTeams:
                t, _ = SportsTeams.objects.get_or_create(
                    interest=team, defaults={"interest": team}
                )
                user.sportsTeams.add(t)
        if likes is not None:
            user.likes.clear()
            for user_id in likes:
                user_ = get_user_model().objects.get(id=user_id)
                if user_ is not None:
                    user.likes.add(user_)
        if book is not None:
            user.book.clear()
            for book_title in book:
                b, _ = Book.objects.get_or_create(
                    interest=book_title, defaults={"interest": book_title}
                )
                user.book.add(b)
        if tvShows is not None:
            user.tvShows.clear()
            for show in tvShows:
                s, _ = TVShow.objects.get_or_create(
                    interest=show, defaults={"interest": show}
                )
                user.tvShows.add(s)
        if zodiacSign is not None:
            user.zodiacSign = zodiacSign
        if interested_in is not None:
            user.interested_in = ",".join(str(i) for i in interested_in)
        if ethinicity is not None:
            user.ethinicity = ethinicity
        if religion is not None:
            user.religion = religion
        if education is not None:
            user.education = education
        if avatar_index is not None:
            user.avatar_index = avatar_index
        if onesignal_player_id is not None:
            user.onesignal_player_id = onesignal_player_id
        if fcm_registration_id is not None:
            GCMDevice.objects.get_or_create(
                registration_id=fcm_registration_id, cloud_message_type="FCM", user=user
            )
        if paste_access is not None:
            user.paste_access = paste_access
        # if allow_manual_chat is not None:
        #     user.allow_manual_chat = allow_manual_chat

        # depricated property
        # if photos is not None:
        #     user.photo_set.all().delete()
        #     for photo in photos:
        #         new_pic = Photo.objects.create(
        #             user=user,
        #             image_data=photo
        #         )
        #         new_pic.save()

        if url is not None or platform is not None:
            if profile is None:
                new_profile = UserSocialProfile.objects.create(
                    url=url, platform=platform, user=user
                )
                new_profile.save()
            else:
                if url is not None:
                    profile.url = url
                    profile.save()
                if platform is not None:
                    profile.platform = platform
                    profile.save()

        user.save()
        send_notification_to_nearby_users.apply_async(args=[str(id)])
        return userResponseObj(id=user.id, username=user.username)


class DeleteProfileResponse(graphene.ObjectType):
    result = graphene.String()


class DeleteProfile(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    Output = DeleteProfileResponse

    def mutate(self, info, id):
        try:
            u = User.objects.get(id=id)
            if info.context.user.id != u.id:
                raise GraphQLError(
                    message="You are not authorized to delete this account"
                )
            else:
                Reported_Users.objects.filter(
                    Q(reporter=u) | Q(reportee=u)).delete()
                u.delete()
                return DeleteProfileResponse(result="Profile deleted.")
        except User.DoesNotExist:
            raise Exception(translate_error_message(
                info.context.user, "Account does not exist"))


#    AuthMutation,


class Mutation(
    user.schema.Mutation,
    reports.schema.Mutation,
    purchase.schema.Mutation,
    payments.schema.Mutation,
    chat.schema.Mutation,
    moments.schema.Mutation,
    gifts.schema.Mutation,
    stock_image.schema.Mutation,
    graphene.ObjectType,
):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    updateProfile = UpdateProfile.Field()
    # depricated due to dangerous use case and unathenticated code
    deleteProfile = DeleteProfile.Field()


class permissionType(graphene.ObjectType):
    has_permission = graphene.Boolean()
    coins_to_unlock = graphene.Int()
    free_user_limit = graphene.Int()


class UserSearchAndPermissionType(graphene.ObjectType):
    user = graphene.List(UserType)
    my_permission = graphene.Field(permissionType)


def get_user_search_permission(permission, user):
    now = timezone.now()
    has_permision = False

    subscription = PackagePurchase.objects.filter(
        user=user, is_active=True, starts_at__lte=now, ends_at__gte=now
    ).first()

    if subscription:
        permissions = [
            *Permission.objects.filter(package=subscription.package).values_list(
                "name", flat=True
            )
        ]
        if permission in permissions:
            has_permision = True
    return has_permision


class Translation(graphene.ObjectType):
    text = graphene.String()
    translated_text = graphene.String()
    language = graphene.String()


class Query(
    # travel_log_data.schema.Query,
    chat.schema.Query,
    defaultPicker.schema.Query,
    user.schema.Query,
    moments.schema.Query,
    payments.schema.Query,
    gifts.schema.Query,
    purchase.schema.Query,
    stock_image.schema.Query,
    reports.schema.Query,
    graphene.ObjectType,
):
    users = graphene.List(UserType, name=graphene.String(required=False))
    user = graphene.Field(UserType, id=graphene.String(required=True))
    translate_text = graphene.Field(Translation, sentence=graphene.String(required=True), target_language=graphene.String(required=True))

    random_users = graphene.Field(
        UserSearchAndPermissionType,
        interested_in=graphene.Int(),
        # interested_in=graphene.Int(required=True),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        gender=graphene.Int(),
        id=graphene.String(),
        start=graphene.Int(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        address=graphene.String(),
        auto_deduct_coin=graphene.Int(),
        description="Search users based on their age, interest, height or gender",
    )
    popular_users = graphene.Field(
        UserSearchAndPermissionType,
        interested_in=graphene.Int(),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        gender=graphene.Int(),
        id=graphene.String(),
        start=graphene.Int(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        auto_deduct_coin=graphene.Int(),
        description="Search users based on their age, interest, height or gender",
    )
    most_active_users = graphene.Field(
        UserSearchAndPermissionType,
        interested_in=graphene.Int(),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        gender=graphene.Int(),
        id=graphene.String(),
        start=graphene.Int(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        auto_deduct_coin=graphene.Int(),
        description="Search users based on their age, interest, height or gender",
    )

    new_users = graphene.List(UserType)

    attr_translation = graphene.List(
        attrTranslationType,
        attr_names=graphene.List(graphene.String, required=True)
    )

    def resolve_translate_text(self, info, sentence, target_language):
        translation = translator.translate(sentence, dest=target_language)
        return Translation(text=sentence, translated_text=translation.text, language=translation.dest)

    def resolve_users(self, info, name=None):
        blocked = info.context.user.blockedUsers.all().values_list("id", flat=True)
        if name:
            blocked_by = info.context.user.blocked_by.all().values_list("id", flat=True)
            return (
                get_user_model()
                .objects.filter(
                    Q(social_auth__isnull=False) | Q(social_auth__isnull=True)
                )
                .filter(fullName__icontains=name)
                .exclude(id__in=blocked)
                .exclude(id__in=blocked_by)
            )
        return (
            get_user_model()
            .objects.filter(Q(social_auth__isnull=False) | Q(social_auth__isnull=True))
            .exclude(id__in=blocked)
        )

    @staticmethod
    def resolve_user(self, info, **kwargs):
        visitor = info.context.user
        id = kwargs.get("id")
        if id is None:
            raise Exception(translate_error_message(
                info.context.user, "id i`s a required parameter"))
        try:
            print(" resolve_user like 599: framework.schema")
            user_obj = get_user_model().objects.get(id=id)
            print("----------------", visitor.roles.all())
            if not visitor.id == user_obj.id and not visitor.roles.filter(role__in=["ADMIN"]):

                profile_visit, created = ProfileVisit.objects.get_or_create(
                    visitor=visitor, visiting=user_obj)

                print(f"User {visitor} visit {user_obj} last notified at: {profile_visit.last_visited_at}")
                if not created and not profile_visit.can_notify_profile_visit:
                    return user_obj
                # Update the last visit time
                profile_visit.last_visited_at = datetime.now()
                profile_visit.save()

                print(f"Preparing for profile visit notification to {user_obj} on visiting user {visitor}")
                icon = None
                try:
                    avatar_url = visitor.avatar().file.url
                except:
                    avatar_url = None

                if avatar_url:
                    icon = info.context.build_absolute_uri(avatar_url)
                notification_setting = "PROFILEVISIT"
                try:
                    moderator = ChatsQue.objects.filter(worker=visitor, isAssigned=True).first().moderator
                except Exception as e:
                    print(e)
                    moderator = visitor

                data = {
                    "notification_type": notification_setting,
                    "visited_user_id": str(moderator.id)
                }
                # send in-app notification and push notification
                notification_obj = Notification.objects.filter(
                    user=user_obj,
                    sender=moderator,
                    notification_setting_id=notification_setting,
                ).order_by('-created_date').first()

                if notification_obj:
                    # Update Same Most recent notification
                    notification_obj.sender = moderator
                    notification_obj.user = user_obj
                    notification_obj.created_date = profile_visit.last_visited_at
                    notification_obj.data = data
                else:
                    notification_obj = Notification(
                        user=user_obj,
                        sender=moderator,
                        notification_setting_id=notification_setting,
                        data=data
                    )

                send_notification_fcm(
                    notification_obj=notification_obj, icon=icon, image=icon)

                ProfileVisitSubscription.broadcast(
                    group=f"{user_obj.id}",
                    payload={'profile_visit_instance': profile_visit}
                )
            return user_obj
        except User.DoesNotExist as e:
            raise Exception(translate_error_message(
                info.context.user, "User doesn't exists.")) from e

    @staticmethod
    def resolve_random_users(self, info, **kwargs):
        interest = kwargs.get("interested_in")
        max_age = kwargs.get("max_age")
        min_age = kwargs.get("min_age")
        max_height = kwargs.get("max_height")
        min_height = kwargs.get("min_height")
        gender = kwargs.get("gender")
        userid = kwargs.get("id")
        start = kwargs.get("start")
        limit = kwargs.get("limit")
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        search_key = kwargs.get("search_key")
        family_plan = kwargs.get("family_plan")
        politics = kwargs.get("politics")
        religious = kwargs.get("religious")
        zodiacSign = kwargs.get("zodiacSign")
        max_distance = kwargs.get("max_distance")
        address = kwargs.get("address")
        auto_deduct_coin = kwargs.get("auto_deduct_coin")

        blocked = info.context.user.blockedUsers.all().values_list("id", flat=True)
        res = get_user_model().objects.all().exclude(id__in=blocked)

        if interest:
            users = get_user_model().objects.all()
            filtered_users = [
                user.id for user in users if interest in user.interestedIn_display
            ]
            filtered_users = list(set(filtered_users))
            res = res.filter(id__in=filtered_users)

        if address:
            res = res.filter(address__contains=address)
        # if latitude:
        #     res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter(~Q(id=userid))

        # if longitude:
        #     res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key and search_key != "":
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                # print(user.location.split(','))
                if "," not in user.location:
                    continue
                user_location = tuple(map(float, user.location.split(",")))
                if not user_location:
                    continue
                if (
                    geopy.distance.distance(base_location, user_location).miles
                    <= max_distance
                ):
                    user.distance = str(
                        int(geopy.distance.distance(
                            base_location, user_location).miles)
                    )
                    user.save()
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)
        else:
            for user in res:
                user.distance = ""
                user.save()

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))

        if gender in [0,1,2]:
            res = res.filter(gender=gender)

        # order the result if the settings is enabled
        user_advanced_sorting = FeatureSettings.get_setting(
            feature_type="user_advanced_sorting", default=0)
        if user_advanced_sorting:
            now = timezone.now()
            res = res.annotate(
                current_subscription=Coalesce(
                    Subquery(
                        PackagePurchase.objects.filter(
                            user=OuterRef('id'), is_active=True,
                            starts_at__lte=now, ends_at__gte=now,
                            renewed_at__isnull=True
                        ).values('package_id')
                    ),
                    Value(0)
                ),
                user_role=F("roles__id") % MODERATOR_ID
            )
            res = res.order_by('user_role', '-current_subscription', '-purchase_coins')
        else:
            res = res.annotate(user_role=F("roles__id") % MODERATOR_ID)
            res = res.order_by('user_role')

        res = res.annotate(user_role=F("roles__role"))
        permission = "RANDOM_SEARCHED_USER_RESULTS_LIMIT"

        has_permision = get_user_search_permission(
            permission, info.context.user)
        coins_to_unlock = 0

        permission_obj = Permission.objects.filter(name=permission).first()
        free_limit = permission_obj.user_free_limit
        unlocked_limit = permission_obj.user_unlocked_result_limit
        res = res[:(free_limit+unlocked_limit)]

        if not has_permision:
            # check if user has paid for this permission within the last 24 hrs
            now = timezone.now()
            unlock_search_purchase = CoinSpendingHistory.objects.filter(
                user=info.context.user,
                description=permission,
                created_at__gte=now-timedelta(days=1)
            )

            if unlock_search_purchase.count() == 0:
                coins = CoinSettings.objects.filter(method=permission).first()
                coins_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coins, region=info.context.user.get_coinsettings_region()
                )
                if coins_for_region.count():
                    coins = coins_for_region.first()

                if auto_deduct_coin and coins and coins.coins_needed > 0:
                    info.context.user.deductCoins(
                        coins.coins_needed, permission)
                    info.context.user.save()
                    has_permision = True
                else:
                    if coins:
                        coins_to_unlock = coins.coins_needed
            else:
                has_permision = True

        if start:
            res = res[start:]

        if limit:
            res = res[:limit]

        return UserSearchAndPermissionType(
            user=res,
            my_permission=permissionType(
                has_permission=has_permision,
                coins_to_unlock=coins_to_unlock,
                free_user_limit=free_limit
            )
        )

    @staticmethod
    def resolve_popular_users(self, info, **kwargs):
        interest = kwargs.get("interested_in")
        max_age = kwargs.get("max_age")
        min_age = kwargs.get("min_age")
        max_height = kwargs.get("max_height")
        min_height = kwargs.get("min_height")
        gender = kwargs.get("gender")
        userid = kwargs.get("id")
        start = kwargs.get("start")
        limit = kwargs.get("limit")
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        search_key = kwargs.get("search_key")
        family_plan = kwargs.get("family_plan")
        politics = kwargs.get("politics")
        religious = kwargs.get("religious")
        zodiacSign = kwargs.get("zodiacSign")
        max_distance = kwargs.get("max_distance")
        auto_deduct_coin = kwargs.get("auto_deduct_coin")

        blocked = info.context.user.blockedUsers.all().values_list("id", flat=True)
        res = get_user_model().objects.all().exclude(id__in=blocked)

        res = res.annotate(
            visitor_count=Count('user_visiting', distinct=True),
            follower_count=Count('user_following', distinct=True),
            popularity=F('visitor_count')+F('follower_count'),
            user_role=F("roles__id") % MODERATOR_ID
        )
        res = res.order_by('-popularity')

        if interest:
            users = (
                get_user_model().objects.all()
            )
            filtered_users = []
            for user in users:
                if interest in user.interestedIn_display:
                    filtered_users.append(user.id)
            filtered_users = list(set(filtered_users))
            res = res.filter(id__in=filtered_users)

        if latitude:
            res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter(~Q(id=userid))
        if longitude:
            res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key and search_key != "":
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                user_location = tuple(map(float, user.location.split(",")))
                if not user_location:
                    continue
                if (
                    geopy.distance.distance(base_location, user_location).miles
                    <= max_distance
                ):
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))

        if gender in [0,1,2]:
            res = res.filter(gender=gender)

        # order the result if the settings is enabled
        user_advanced_sorting = FeatureSettings.get_setting(
            feature_type="user_advanced_sorting", default=0)
        if user_advanced_sorting:
            now = timezone.now()
            res = res.annotate(
                current_subscription=Coalesce(
                    Subquery(
                        PackagePurchase.objects.filter(
                            user=OuterRef('id'), is_active=True,
                            starts_at__lte=now, ends_at__gte=now,
                            renewed_at__isnull=True
                        ).values('package_id')
                    ),
                    Value(0)
                )
            )
            res = res.order_by('user_role','-current_subscription', '-purchase_coins')
        else:
            res = res.order_by('user_role','-popularity')
        permission = "POPULAR_SEARCHED_USER_RESULTS_LIMIT"

        has_permision = get_user_search_permission(
            permission, info.context.user)
        coins_to_unlock = 0

        permission_obj = Permission.objects.filter(name=permission).first()
        free_limit = permission_obj.user_free_limit
        unlocked_limit = permission_obj.user_unlocked_result_limit
        res = res[:(free_limit+unlocked_limit)]

        if not has_permision:
            # check if user has paid for this permission within the last 24 hrs
            now = timezone.now()
            unlock_search_purchase = CoinSpendingHistory.objects.filter(
                user=info.context.user,
                description=permission,
                created_at__gte=now-timedelta(days=1)
            )

            if unlock_search_purchase.count() == 0:
                coins = CoinSettings.objects.filter(method=permission).first()
                coins_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coins, region=info.context.user.get_coinsettings_region()
                )
                if coins_for_region.count():
                    coins = coins_for_region.first()

                if auto_deduct_coin and coins and coins.coins_needed > 0:
                    info.context.user.deductCoins(
                        coins.coins_needed, permission)
                    info.context.user.save()
                    has_permision = True
                else:
                    if coins:
                        coins_to_unlock = coins.coins_needed
            else:
                has_permision = True

        if start:
            res = res[start:]

        if limit:
            res = res[:limit]

        return UserSearchAndPermissionType(
            user=res,
            my_permission=permissionType(
                has_permission=has_permision,
                coins_to_unlock=coins_to_unlock,
                free_user_limit=free_limit
            )
        )

    @staticmethod
    def resolve_most_active_users(self, info, **kwargs):
        interest = kwargs.get("interested_in")
        max_age = kwargs.get("max_age")
        min_age = kwargs.get("min_age")
        max_height = kwargs.get("max_height")
        min_height = kwargs.get("min_height")
        gender = kwargs.get("gender")
        userid = kwargs.get("id")
        start = kwargs.get("start")
        limit = kwargs.get("limit")
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        search_key = kwargs.get("search_key")
        family_plan = kwargs.get("family_plan")
        politics = kwargs.get("politics")
        religious = kwargs.get("religious")
        zodiacSign = kwargs.get("zodiacSign")
        max_distance = kwargs.get("max_distance")
        auto_deduct_coin = kwargs.get("auto_deduct_coin")

        blocked = info.context.user.blockedUsers.all().values_list("id", flat=True)
        res = get_user_model().objects.all().exclude(id__in=blocked)

        res = res.annotate(
            chat_message_count=Count('Sender', distinct=True),
            story_count=Count('story', distinct=True),
            # moment_count=Count('User_for_moments', distinct=True),
            # story_comment_count=Count('user_comments', distinct=True),
            # story_like_count=Count('user_likes', distinct=True),
            # moment_comment_count=Count('User_for_comment', distinct=True),
            # moment_like_count=Count('User_for_like', distinct=True),
            follow_count=Count('user_follower', distinct=True),
            visit_count=Count('user_visitor', distinct=True),
            user_role=F("roles__id") % MODERATOR_ID
        )
        # res = res.annotate(moment_count=Count('User_for_moments', distinct=True))

        res = res.annotate(activity_count=F('chat_message_count') +
                           F('story_count') +
                           # F('moment_count')+
                           # F('story_comment_count')+
                           # F('story_like_count')+
                           # F('moment_comment_count')+F('moment_like_count')+
                           F('follow_count')+F('visit_count')
                           )
        res = res.order_by('user_role', '-isOnline', '-activity_count')

        if interest:
            users = get_user_model().objects.all()
            filtered_users = []
            for user in users:
                if interest in user.interestedIn_display:
                    filtered_users.append(user.id)
            filtered_users = list(set(filtered_users))
            res = res.filter(id__in=filtered_users)

        if latitude:
            res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter(~Q(id=userid))
        if longitude:
            res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key and search_key != "":
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                user_location = tuple(map(float, user.location.split(",")))
                if not user_location:
                    continue
                if (
                    geopy.distance.distance(base_location, user_location).miles
                    <= max_distance
                ):
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))
        res = res.filter(isOnline=True)

        if gender in [0,1,2]:
            res = res.filter(gender=gender)

        # order the result if the settings is enabled
        user_advanced_sorting = FeatureSettings.get_setting(
            feature_type="user_advanced_sorting", default=0)
        if user_advanced_sorting:
            now = timezone.now()
            res = res.annotate(
                current_subscription=Coalesce(
                    Subquery(
                        PackagePurchase.objects.filter(
                            user=OuterRef('id'), is_active=True,
                            starts_at__lte=now, ends_at__gte=now,
                            renewed_at__isnull=True
                        ).values('package_id')
                    ),
                    Value(0)
                )
            )
            res = res.order_by('user_role', '-current_subscription', '-purchase_coins')
        permission = "MOST_ACTIVE_SEARCHED_USER_RESULTS_LIMIT"

        has_permision = get_user_search_permission(
            permission, info.context.user)
        coins_to_unlock = 0

        permission_obj = Permission.objects.filter(name=permission).first()
        free_limit = permission_obj.user_free_limit
        unlocked_limit = permission_obj.user_unlocked_result_limit
        res = res[:(free_limit+unlocked_limit)]

        if not has_permision:
            # check if user has paid for this permission within the last 24 hrs
            now = timezone.now()
            unlock_search_purchase = CoinSpendingHistory.objects.filter(
                user=info.context.user,
                description=permission,
                created_at__gte=now-timedelta(days=1)
            )

            if unlock_search_purchase.count() == 0:
                coins = CoinSettings.objects.filter(method=permission).first()
                coins_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=coins, region=info.context.user.get_coinsettings_region()
                )
                if coins_for_region.count():
                    coins = coins_for_region.first()

                if auto_deduct_coin and coins and coins.coins_needed > 0:
                    info.context.user.deductCoins(
                        coins.coins_needed, permission)
                    info.context.user.save()
                    has_permision = True
                else:
                    if coins:
                        coins_to_unlock = coins.coins_needed
            else:
                has_permision = True

        if start:
            res = res[start:]

        if limit:
            res = res[:limit]

        return UserSearchAndPermissionType(
            user=res,
            my_permission=permissionType(
                has_permission=has_permision,
                coins_to_unlock=coins_to_unlock,
                free_user_limit=free_limit
            )
        )

    def resolve_new_users(self, info, **kwargs):
        days = Settings.get_setting(key="new_users_num_of_days", default=1)
        hours = int(days) * 24
        delta = datetime.now() - timedelta(hours=hours)

        return (
            get_user_model()
            .objects.filter(created_at__gte=delta)
            .exclude(
                id=info.context.user.id,
                roles__role__in=["CHATTER", "ADMIN", "MODERATOR"],
            )
        )

    def resolve_attr_translation(self, info, **kwargs):
        attr_names = kwargs.get("attr_names")
        all_translations = []
        attr_names_flag = {}

        name_translations = UserProfileTranlations.objects.filter(
            name__in=attr_names)

        for attr_name in attr_names:
            attr_names_flag[attr_name] = False
        for name_translation in name_translations:
            name = name_translation.name
            name_translated = getattr(
                name_translation, translated_field_name(info.context.user, "name"))
            attr_names_flag[name] = True
            all_translations.append(attrTranslationType(
                name=name, name_translated=name_translated))
        for attr_name in attr_names:
            if not attr_names_flag[attr_name]:
                all_translations.append(attrTranslationType(
                    name=attr_name, name_translated=""))

        return all_translations


class ProfileViewMiddleware:
    def resolve(self, next_middleware, root, info, **args):
        # Call the next middleware in the chain
        result = next_middleware(root, info, **args)
        print("in the middleware ===========================")
        # Get the authenticated user and the viewed user
        visitor = info.context.user
        visiting = result

        # Create the new profile view
        if viewer.is_authenticated and viewed_user != viewer:
            print("createedddd user===============================")
            # ProfileView.objects.create(viewer=viewer, viewed_user=viewed_user)

        # Return the result
        return result


class Subscription(
    chat.schema.Subscription,
    moments.schema.Subscription,
    user.schema.Subscription,
    payments.schema.Subscription,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope["user"] = await channels.auth.get_user(self.scope)
        # self.scope['auth_user'] , _ = await TokenAuthentication().authenticate(self.scope)
        # print(self.scope['subprotocol'])
