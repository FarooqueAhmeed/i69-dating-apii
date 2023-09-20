import datetime

import graphene
import requests
from dj_rest_auth.serializers import TokenSerializer
from dj_rest_auth.utils import default_create_token
from django.contrib.auth import get_user_model
from requests_oauthlib import OAuth1
from rest_framework.authtoken.models import Token
from social.apps.django_app.default.models import UserSocialAuth

from reports.models import GoogleAuth, Reported_Users, SocialAuthDetail
from user.models import User, settings
from user.utils import translate_error_message
from graphene_django import DjangoObjectType

def get_token(user):
    if not user:
        return ""
    token = default_create_token(Token, user, TokenSerializer)
    return token.key


class reportResponseObj(graphene.ObjectType):
    id = graphene.String()


class reportUser(graphene.Mutation):
    class Arguments:
        reporter = graphene.String(required=True)
        reportee = graphene.String(required=True)
        reason = graphene.String(required=True)

    Output = reportResponseObj

    def mutate(self, info, reporter, reportee, reason):
        User = get_user_model()

        try:
            reporter_user = User.objects.get(id=reporter)
            reportee_user = User.objects.get(id=reportee)
        except Exception:
            raise Exception(translate_error_message(info.context.user, "User does not exist"))

        if reporter_user == reportee_user:
            raise Exception(translate_error_message(info.context.user, "You can not report yourself"))

        report = Reported_Users.objects.create(
            reporter=reporter_user, reportee=reportee_user, reason=reason
        )
        print(Reported_Users.id)
        return reportResponseObj(id=report.id)


class googleAuthResponse(graphene.ObjectType):
    email = graphene.String()
    is_new = graphene.Boolean()
    id = graphene.String()
    token = graphene.String()
    username = graphene.String()


class twitterAuthResponse(graphene.ObjectType):
    twitter = graphene.String()
    username = graphene.String()
    is_new = graphene.Boolean()
    id = graphene.String()
    token = graphene.String()


def check_is_new(user: User):
    """
    Check whether a user is not properly initialized
    """
    if (
        user.age == None
        or user.fullName == ""
        or user.height == None
        or user.avatar_photos.all().count() == 0
    ):
        return True
    return False


class SocialAuth(graphene.Mutation):
    class Arguments:
        access_token = graphene.String(required=True)
        provider = graphene.String(required=True)
        access_verifier = graphene.String(default_value="")

    Output = googleAuthResponse

    def mutate(self, info, access_token, provider, access_verifier=""):
        try:

            if "google" in provider.lower():
                idinfo = requests.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={access_token}"
                )
                idinfo = idinfo.json()
                if idinfo.get("error") == "invalid_token":
                    return Exception(translate_error_message(info.context.user, "Invalid Token"))
            if "facebook" in provider.lower():
                redirect_url = "https://api.i69app.com"
                # idinfo = requests.get(
                #     f"https://graph.facebook.com/oauth/access_token?client_id=1610603699070152&client_secret=cc752b4e78233fe6df148dc6305fb6d0&grant_type=client_credentials&redirect_uri={redirect_url}")
                idinfo = requests.get(
                    f"https://graph.facebook.com/me?fields=name,email&access_token={access_token}"
                )
                idinfo = idinfo.json()
                if idinfo.get("error") == "invalid_token":
                    return Exception(translate_error_message(info.context.user, "Invalid Token"))

            # ==========================================
            if "apple" in provider.lower():
                if access_verifier == "":
                    access_verifier_check = UserSocialAuth.objects.filter(
                        extra_data=access_token
                    )
                    if access_verifier_check.count() > 0:
                        access_verifier_check = UserSocialAuth.objects.get(
                            extra_data=access_token
                        )
                        access_verifier = access_verifier_check.uid
                    else:
                        return Exception(translate_error_message(info.context.user, "Email is required for first sign in."))
                userCnt = get_user_model().objects.filter(email=access_verifier).count()
                if userCnt > 0:
                    user = get_user_model().objects.get(email=access_verifier)
                    is_new = check_is_new(user)
                else:
                    user, _ = get_user_model().objects.get_or_create(
                        email=access_verifier,
                        defaults={
                            "password": "",
                            "fullName": "",
                            # "fullName": access_verifier,
                            "email": access_verifier,
                            "username": access_verifier.replace("@", "_"),
                        },
                    )
                    user.last_login = datetime.datetime.now()
                    user.save()

                    socialAuth, _ = UserSocialAuth.objects.get_or_create(
                        user_id=user.id,
                        defaults={
                            "provider": provider.lower(),
                            "uid": access_verifier,
                            "user_id": user.id,
                            "extra_data": access_token,
                        },
                    )
                    socialAuth.save()

                    is_new = True
                return googleAuthResponse(
                    email=access_verifier,
                    is_new=is_new,
                    id=user.id,
                    token=get_token(user),
                    username=access_verifier.replace("@", "_"),
                )
            # ============================================================

            if "twitter" in provider.lower():

                oauth = OAuth1(
                    settings.SOCIAL_AUTH_TWITTER_KEY,
                    client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                    resource_owner_key=access_token,
                    verifier=access_verifier,
                )
                res = requests.post(
                    f"https://api.twitter.com/oauth/access_token", auth=oauth
                )
                print(res.text)
                res_split = res.text.split("&")
                if len(res_split) >= 4:
                    oauth_token = res_split[0].split("=")[1]
                    oauth_secret = res_split[1].split("=")[1]
                    user_id = res_split[2].split("=")[1] if len(res_split) > 2 else None
                    user_name = (
                        res_split[3].split("=")[1] if len(res_split) > 3 else None
                    )
                else:
                    return Exception(res.text)

                if user_id == None or user_name == None:
                    return Exception(translate_error_message(info.context.user, "Invalied token"))
                else:
                    try:
                        user = get_user_model().objects.get(twitter=user_id)
                        is_new = check_is_new(user)
                    except:
                        user, _ = get_user_model().objects.get_or_create(
                            twitter=user_id,
                            defaults={
                                "password": "",
                                "fullName": user_name,
                                "email": user_id + "@twitter.com",
                                "username": user_name + "_twitter",
                            },
                        )
                        user.last_login = datetime.datetime.now()
                        user.save()
                        is_new = True
                        socialAuth, _ = UserSocialAuth.objects.get_or_create(
                            user_id=user.id,
                            defaults={
                                "provider": provider.lower(),
                                "uid": user_id,
                                "user_id": user.id,
                                "extra_data": "",
                            },
                        )
                        socialAuth.save()

                    return twitterAuthResponse(
                        twitter=user_id,
                        is_new=is_new,
                        id=user.id,
                        token=get_token(user),
                        username=user.username,
                    )

            userCnt = get_user_model().objects.filter(email=idinfo["email"]).count()
            if userCnt > 0:
                user = get_user_model().objects.get(email=idinfo["email"])
                is_new = check_is_new(user)
                user.last_login = datetime.datetime.now()
                user.save()
            else:
                user, _ = get_user_model().objects.get_or_create(
                    email=idinfo["email"],
                    defaults={
                        "password": "",
                        "fullName": idinfo["name"],
                        "email": idinfo["email"],
                        "username": idinfo["email"].replace("@", "_"),
                    },
                )
                user.last_login = datetime.datetime.now()
                user.save()

                socialAuth, _ = UserSocialAuth.objects.get_or_create(
                    user_id=user.id,
                    defaults={
                        "provider": provider.lower(),
                        "uid": idinfo["email"],
                        "user_id": user.id,
                        "extra_data": "",
                    },
                )
                socialAuth.save()

                is_new = True
                g = GoogleAuth.objects.create(
                    email=idinfo["email"], sub=idinfo.get("sub")
                )
                g.save()

            return googleAuthResponse(
                email=idinfo["email"],
                is_new=is_new,
                id=user.id,
                token=get_token(user),
                username=idinfo["email"].replace("@", "_"),
            )
        except ValueError:
            Exception(translate_error_message(info.context.user, "Invalid Token"))


class SocialAuthUpdateResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()


class SocialAuthDetailType(DjangoObjectType):
    class Meta:
        model = SocialAuthDetail
        fields = "__all__"


class SocialAuthStatusEnum(graphene.Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ADDSocialAuthMutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        provider = graphene.String(required=True)
        status = SocialAuthStatusEnum(required=True)

    social_auth = graphene.Field(SocialAuthDetailType)

    @classmethod
    def mutate(cls, root, info, provider, status):
        user = info.context.user
        if provider.lower() not in ['google', 'facebook', 'twitter', 'apple']:
            raise Exception(translate_error_message(info.context.user, "Platform unknown!"))
        new_report = SocialAuthDetail(provider=provider, status=status)
        new_report.save()
        return ADDSocialAuthMutation(social_auth=new_report)

class UpdateSocialAuthMutation(graphene.Mutation):
    Output = SocialAuthUpdateResponse

    class Arguments:
        id = graphene.Int(required=True)
        status = SocialAuthStatusEnum(required=True)

    def mutate(self, info, id, status):
        muser = info.context.user
        try:
            social_auth = SocialAuthDetail.objects.get(id=id)
            social_auth.status = status
            social_auth.save()
            return SocialAuthUpdateResponse(
                success=True, message=translate_error_message(info.context.user, "Social Auth Instance Updated Successfully!")
            )
        except:
            return SocialAuthUpdateResponse(success=False, message=translate_error_message(info.context.user, "Social Auth Instance not found!"))


class DeleteSocialAuthMutation(graphene.Mutation):

    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            delete_social = SocialAuthDetail.objects.get(id=id)
            delete_social.delete()
            return DeleteSocialAuthMutation(success="deleted successfully", id=id)

        except Exception as e:
            raise Exception(translate_error_message(info.context.user, "invalid social auth instance id"))


class Mutation(graphene.ObjectType):
    social_auth = SocialAuth.Field()
    reportUser = reportUser.Field()
    create_social_auth_detail = ADDSocialAuthMutation.Field()
    update_social_auth_detail = UpdateSocialAuthMutation.Field()
    delete_social_auth_detail = DeleteSocialAuthMutation.Field()

class Query(graphene.ObjectType):
    all_social_auth_status = graphene.List(SocialAuthDetailType)

    def resolve_all_social_auth_status(self, info, **kwargs):
        return SocialAuthDetail.objects.all().order_by("-timestamp")
