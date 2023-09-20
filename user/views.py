from dj_rest_auth.views import LoginView
from django.db.models import Subquery
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.app_settings import TokenSerializer, create_token
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
from django.db.models import Count
import django_filters.rest_framework
from rest_framework import filters
from django.utils import timezone
from user.filters import UserFilter, ModeratorFilter, WorkerFilter
from user.models import (
    User,
    UserPhoto,
    UserRole,
    CoinSettings,
    PrivateUserPhoto,
    CoinSettingsForRegion,
)
from worker.models import WorkerInvitation
from user import serializers
from defaultPicker.models import age
from moments.utils import detect_user_image
from stock_image.models import StockImage


class TokenLoginView(LoginView):
    def login(self):
        self.user = self.serializer.validated_data["user"]
        self.token = create_token(
            self.token_model,
            self.user,
            self.serializer,
        )

        if getattr(settings, "REST_SESSION_LOGIN", True):
            self.process_login()

    def get_response(self):
        token_serializer = TokenSerializer(
            instance=self.token, context=self.get_serializer_context()
        )
        user_details_serializer = serializers.UserSerializer(
            instance=self.user, context=self.get_serializer_context()
        )
        user_details_serializer.update(
            instance=self.user,
            validated_data={"isOnline": True,
                            "user_last_seen": timezone.now()},
        )
        data = {
            "user": user_details_serializer.data,
            "key": token_serializer.data["key"],
        }
        return Response(data, status=status.HTTP_200_OK)


class UserListView(
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticated]
    # queryset = (
    #     User.objects.all()
    #     .annotate(roles_count=Count("roles"))
    #     .filter(Q(roles_count=0) and ~Q(email__endswith="i69app.com"))
    #     .filter(is_staff=False)
    #     .filter(is_superuser=False)
    # )
    queryset = (
        User.objects.filter(
            ~Q(roles__role__in=["CHATTER", "ADMIN", "MODERATOR"]),
            ~Q(email__endswith="i69app.com"),
            Q(is_staff=False),
            Q(is_superuser=False)
        ).order_by("-created_at")
    )

    serializer_class = serializers.UserSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = UserFilter
    filterset_fields = []
    search_fields = ["email", "fullName"]


user_list_view = UserListView.as_view()


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


user_detail_view = UserDetailView.as_view()


class WorkerListView(
    generics.ListAPIView,
):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.filter(
        pk__in=Subquery(
            User.objects.filter(Q(roles__role__in=["CHATTER"])).all().distinct('id').values('pk')
        )
    ).all()

    serializer_class = serializers.UserSerializer
    filterset_class = WorkerFilter
    filterset_fields = []
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering_fields = ["created_at"]
    ordering = "-created_at"  # Default sorting order

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]


class ModeratorListView(
    generics.ListAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(
        pk__in=Subquery(
            User.objects.filter(Q(roles__role__in=["MODERATOR"])).all().distinct('id').values('pk')
        )
    ).all()

    serializer_class = serializers.UserSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter
    ]
    filterset_class = ModeratorFilter
    filterset_fields = []
    search_fields = ["email", "fullName"]
    ordering_fields = ["created_at"]
    ordering = "-created_at"  # Default sorting order


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(fullName__icontains=name)
        return queryset


class AdminListView(
    generics.ListAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(
        pk__in=Subquery(
            User.objects.filter(Q(roles__role__in=["ADMIN"])).all().distinct('id').values('pk')
        )
    ).all()

    serializer_class = serializers.UserSerializer

    filterset_class = WorkerFilter
    filterset_fields = []
    ordering_fields = ["created_at"]
    ordering = "-created_at"  # Default sorting order
    search_fields = ['email', 'first_name', 'last_name', 'username']

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]


admin_list_view = AdminListView.as_view()
worker_list_view = WorkerListView.as_view()
moderator_list_view = ModeratorListView.as_view()


class GenerateWorkerInvitationView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, key=""):
        print(key)
        try:
            invitation = WorkerInvitation.objects.filter(token=key)
        except ValidationError:
            return Response({"messsage": f"{key} is not a valid UUID"}, status=400)
        if len(invitation) == 0:
            return Response({"message": "invalid invitation key"}, status=401)
        invitation = invitation[0]
        return Response({"email": invitation.email, "key": key})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({}, status=401)
        roles = [r.role for r in request.user.roles.all()]
        if "ADMIN" not in roles and "SUPER_ADMIN" not in roles:
            return Response({}, status=401)
        data = request.data
        data.pop("generated", None)
        data.pop("link_value", None)
        token = uuid.uuid4()
        email = request.data.get("email", None)
        is_admin_permission = request.data.get("is_admin_permission", None)
        is_chat_admin_permission = request.data.get(
            "is_chat_admin_permission", None)
        if (
            email != None
            and is_admin_permission != None
            and is_chat_admin_permission != None
        ):
            invitation = WorkerInvitation(token=token, **data)
            invitation.save()
            return Response({"link": f"/#/signUp/?invitationKey={token}"})
        else:
            return Response(
                {
                    "message": "email, is_admin_permission and is_chat_admin_permission required"
                },
                status=400,
            )


generate_worker_invitation_view = GenerateWorkerInvitationView.as_view()


def authorize_is_worker_or_owner(request, id):
    # authorization
    if str(request.user.id) != id and len(request.user.roles.all()) == 0:
        return Response(
            {"reason": "You are not authorized to upload photo for this user"},
            status=401,
        )


class PhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        res = authorize_is_worker_or_owner(request, id)
        if res:
            return res
        roles = {r.role for r in request.user.roles.all()}
        user = request.user

        photo_id = request.data.get("id")
        type = request.data.get("type", "PUBLIC")
        if type == "PUBLIC":
            photo = get_object_or_404(UserPhoto, id=photo_id)
            if len(roles) == 0:  # check for users that are not worker
                if photo.user.id != request.user.id:
                    return Response({}, status=401)
            if "CHATTER" in roles:
                if not user.fake_users.filter(id=photo.user.id).exists():
                    return Response("Moderator do not belongs to you", status=401)
                user = photo.user
            if user.avatar_photos.all().count() < 2:
                return Response("Atleast one photo must be present", status=403)
        else:
            photo = get_object_or_404(PrivateUserPhoto, id=photo_id)
            if photo.user.id != request.user.id:
                return Response({}, status=401)
        photo.delete()
        return Response({})

    def post(self, request, id):
        try:
            res = authorize_is_worker_or_owner(request, id)
            if res:
                return res

            type = request.data.get("type", "PUBLIC")

            user = get_object_or_404(User, id=id)
            # check count of already uploaded photos
            if type == "PUBLIC":
                if user.avatar_photos.count() >= user.photos_quota:
                    roles = {r.role for r in request.user.roles.all()}
                    if "ADMIN" not in roles:
                        coin_setting = CoinSettings.objects.get(
                            method="Photo & file - attached in Chat"
                        )
                        coins_for_region = CoinSettingsForRegion.objects.filter(
                            coinsettings=coin_setting, region=user.get_coinsettings_region()
                        )
                        if coins_for_region.count():
                            coin_setting = coins_for_region.first()

                        if user.coins < coin_setting.coins_needed:
                            return Response(
                                {
                                    "reason": f"Require {coin_setting.coins_needed} coins to upload more than 4 photos"
                                },
                                status=401,
                            )
                        else:
                            print(user.coins)
                            user.deductCoins(
                                coin_setting.coins_needed, "Photo & file - attached in Chat")
                            user.save()

            url = ""
            photo = request.data.get("photo", None)
            img_url = request.data.get("url", None)
            stock_image_id = request.data.get("stock_image_id", None)
            if not (photo or stock_image_id) and not img_url:
                return Response(
                    {"reason": "photo/stockId or url form-data required"}, status=400
                )

            if type == "PUBLIC":
                if stock_image_id:
                    try:
                        photo = StockImage.objects.get(id=stock_image_id).file
                    except:
                        return Response(
                            {"reason": "Invalid stock Image Id"}, status=400
                        )
                if photo:
                    up = UserPhoto(file=photo, user=user)
                    up.save()
                    if not stock_image_id:
                        detect_user_image(up)
                    up = UserPhoto.objects.get(id=up.id)
                    if up.file:
                        url = request.build_absolute_uri(up.file.url)
                    else:
                        up.delete()
                        up = None
                else:
                    url = img_url
                    up = UserPhoto(file_url=url, user=user)
                    up.save()
                    detect_user_image(up)
                    up = UserPhoto.objects.get(id=up.id)
                    if up.file is None:
                        up.delete()
                        up = None
            elif type == "PRIVATE":
                if stock_image_id:
                    try:
                        photo = StockImage.objects.get(id=stock_image_id).file
                    except:
                        return Response(
                            {"reason": "Invalid stock Image Id"}, status=400
                        )
                if photo:
                    up = PrivateUserPhoto(file=photo, user=user)
                    up.save()
                    up = PrivateUserPhoto.objects.get(id=up.id)
                    url = request.build_absolute_uri(up.file.url)
                else:
                    url = img_url
                    up = PrivateUserPhoto(file_url=url, user=user)
                    up.save()
                    up = PrivateUserPhoto.objects.get(id=up.id)
            user.save()

            if up:
                return Response({"url": url, "id": up.id})
            else:
                return Response({"url": "", "id": ""})
        except Exception as e:
            return Response({"reason": f"unkown exception: {e}"}, status=500)


photo_upload_view = PhotoUploadView.as_view()


class WorkerSignupView(APIView):
    def post(self, request):
        try:
            language = request.data.get("language")
            serializer = serializers.SignUpRequestSerialzier(request.data)
            data = serializer.data
            key = data.pop("invitation_key")
            invitation = WorkerInvitation.objects.filter(token=key)
        except ValidationError as e:
            return Response(e, status=400)

        if len(invitation) == 0:
            return Response({"message": "invalid invitaion key"}, status=400)
        invitation = invitation[0]
        data["email"] = invitation.email
        data["username"] = data["first_name"] + data["last_name"]
        # data.pop("first_name")
        # data.pop("last_name")
        password = data.pop("password")
        try:
            user = User(**data)
            user.set_password(password)
            user.save()

            if invitation.is_admin_permission:
                user.language.set(language)
                user.roles.add(UserRole.objects.get(role=UserRole.ROLE_ADMIN))
            if invitation.is_chat_admin_permission:
                user.language.set(language)
                lg_code = ""
                # print(user.language.all())
                for l in user.language.all():
                    lg_code += (l.language_code).upper() + "-"
                print("lg code = ", lg_code)
                last_worker = User.objects.filter(
                    roles__role__in=["CHATTER"], worker_id_code__gt=0
                ).order_by("worker_id_code")
                print("last wroker", last_worker)
                if last_worker.count() == 0:
                    user.worker_id_code = 1
                else:
                    user.worker_id_code = last_worker.last().worker_id_code + 1
                user.language_id_code = f"{lg_code}{user.worker_id_code:07n}"
                user.roles.add(UserRole.objects.get(
                    role=UserRole.ROLE_CHATTER))
                user.roles.add(UserRole.objects.get(
                    role=UserRole.ROLE_REGULAR))
            user.save()

            return Response(serializers.UserSerializer(user).data, status=201)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=500)


worker_signup_view = WorkerSignupView.as_view()


class UserLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, friend_id):
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 and not request.user.is_superuser:
            return Response({}, status=401)
        user1 = get_object_or_404(User, id=id)
        user2 = get_object_or_404(User, id=friend_id)
        if user2 in user1.likes.all():
            return Response({"message": "like connection already exists"}, status=200)
        user1.likes.add(user2)
        user2.likes.add(user1)
        user1.save()
        user2.save()
        return Response({"message": "created like connection"}, status=201)


user_like_view = UserLikeView.as_view()


class DeleteReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 and not request.user.is_superuser:
            return Response({}, status=401)
        user = get_object_or_404(User, id=id)
        user.reports.all().delete()
        return Response({}, status=200)


delete_reports_view = DeleteReportsView.as_view()


class TransferModeratorView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 or not "ADMIN" in roles:
            return Response({"message": "Unauthorized access"}, status=401)
        # user = get_object_or_404(User, id=id)
        # user.reports.all().delete()
        data = request.data
        worker_id = data.get("worker_id")
        moderator_id = data.get("moderator_id")
        print(not worker_id, moderator_id)
        if not worker_id:
            return Response(
                {"worker_id": "'worker_id' is required"},
                status=400,
            )
        if not moderator_id:
            return Response(
                {"moderator_id": "'moderator_id' is required"},
                status=400,
            )

        try:
            worker = User.objects.get(id=worker_id)
            w_roles = {r.role for r in worker.roles.all()}
            if not ("CHATTER" in w_roles and "REGULAR" in w_roles):
                return Response(
                    {"worker_id": "Invalid 'worker_id'"},
                    status=400,
                )
        except User.DoesNotExist:
            return Response(
                {"worker_id": "Invalid 'worker_id'"},
                status=400,
            )

        try:
            moderator = User.objects.get(id=moderator_id)
            m_roles = {r.role for r in moderator.roles.all()}
            if not "MODERATOR" in m_roles:
                return Response(
                    {"moderator_id": "Invalid 'moderator_id'"},
                    status=400,
                )
        except User.DoesNotExist:
            return Response(
                {"moderator_id": "Invalid 'moderator_id'"},
                status=400,
            )

        if moderator not in worker.fake_users.all():
            if moderator.owned_by.all():
                old_owner = moderator.owned_by.all()[0]
                moderator.owned_by.remove(old_owner)
            worker.fake_users.add(moderator)

        return Response(serializers.UserSerializer(instance=worker).data, status=200)


transfer_moderator_view = TransferModeratorView.as_view()


class DeleteAdminOrModeratorView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        roles = {r.role for r in request.user.roles.all()}
        if len(roles) == 0 and not "ADMIN":
            return Response({"message": "Unauthorized access"}, status=401)

        user = get_object_or_404(User, id=id)
        if user == request.user:
            return Response({"message": "Can not delete itself"}, status=400)

        user_roles = {r.role for r in user.roles.all()}
        if not ("ADMIN" in user_roles or "MODERATOR" in user_roles):
            return Response(
                {"message": "Invalid user_id, should be of ADMIN or MODERATOR"},
                status=400,
            )

        user.delete()
        return Response({}, status=200)


delete_admin_or_moderatorv_view = DeleteAdminOrModeratorView.as_view()


class storyViews(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


user_story_view = storyViews.as_view()