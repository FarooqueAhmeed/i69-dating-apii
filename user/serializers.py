from django.db.models import query

# from defaultPicker.models import language
from rest_framework.exceptions import server_error
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from moments.models import StoryReport

from subscriptions.models import ModeratorSubscriptionPlan
from user.models import User, UserPhoto, UserRole, ModeratorOnlineScheduler
from defaultPicker import models as pickerModels
from reports.serializers import ReportSerializer
import uuid
from django.utils import timezone
from .utils import get_country_from_geo_point


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["firstName"] = user.first_name
        token["lastName"] = user.last_name
        token["privileges"] = {r.role: True for r in user.roles.all()}
        return token


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = UserPhoto

class StoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = StoryReport


class SlugRelatedGetOrCreateField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail("invalid")


class ModeratorOnlineSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorOnlineScheduler
        fields = [
            "id",
            "list_name",
            "online_time",
            "offline_time",
        ]


class LocationSerializerField(serializers.Field):

    def to_representation(self, obj):
        # Convert the location string to the list of lat, lon
        if obj:
            try:
                return [float(loc.strip()) for loc in obj.split(",")]
            except Exception:
                return []

    def to_internal_value(self, data):
        if type(data) is list:
            return ",".join([str(v) for v in data])
        return data


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="fullName")
    reports = ReportSerializer(many=True, read_only=True)
    sign_up = serializers.DateTimeField(source="created_at", read_only=True)
    owner_id = serializers.CharField(max_length=36, write_only=True, required=False)
    gender = serializers.IntegerField(required=True)
    # fake_users = RecursiveField(many=True)
    fake_users = serializers.SerializerMethodField()
    moderatorOnlineList = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(slug_field="role", many=True, read_only=True)
    # owned_by = serializers.SerializerMethodField()
    avatar_photos = UserPhotoSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=pickerModels.tags.objects.all()
    )
    language = serializers.PrimaryKeyRelatedField(
        many=True, queryset=pickerModels.Language.objects.all()
    )
    books = SlugRelatedGetOrCreateField(
        slug_field="interest",
        many=True,
        source="book",
        required=False,
        queryset=pickerModels.book.objects.all(),
    )
    sportsTeams = SlugRelatedGetOrCreateField(
        slug_field="interest",
        many=True,
        required=False,
        queryset=pickerModels.sportsTeams.objects.all(),
    )
    tvShows = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, required=False, queryset=pickerModels.tvShows.objects.all()
    )
    music = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, required=False, queryset=pickerModels.music.objects.all()
    )
    movies = SlugRelatedGetOrCreateField(
        slug_field="interest", many=True, required=False, queryset=pickerModels.movies.objects.all()
    )

    age = serializers.PrimaryKeyRelatedField(
        queryset=pickerModels.age.objects.all(), required=False, allow_null=True
    )
    # language = serializers.PrimaryKeyRelatedField(
    #     queryset=pickerModels.language.objects.all(), required=True, allow_null=False
    # )
    # moderatorOnlineList = serializers.PrimaryKeyRelatedField(
    #     queryset=ModeratorOnlineScheduler.objects.all(), required=False, allow_null=True
    # )
    height = serializers.PrimaryKeyRelatedField(
        queryset=pickerModels.height.objects.all(), required=False, allow_null=True
    )
    ethnicity = serializers.IntegerField(allow_null=True, source="ethinicity")
    subscription_id = serializers.CharField(required=False, write_only=True)
    # ethinicity = serializers.PrimaryKeyRelatedField(queryset=pickerModels.ethnicity.objects.all(), required=False, allow_null=True)
    # zodiacSign = serializers.PrimaryKeyRelatedField(queryset=pickerModels.zodiacSign.objects.all(), required=False, allow_null=True)
    # familyPlans = serializers.PrimaryKeyRelatedField(queryset=pickerModels.family.objects.all(), required=False, allow_null=True)
    # politics = serializers.PrimaryKeyRelatedField(queryset=pickerModels.politics.objects.all(), required=False, allow_null=True)
    # religion = serializers.PrimaryKeyRelatedField(queryset=pickerModels.religious.objects.all(), required=False, allow_null=True)

    stories = serializers.SerializerMethodField()

    location = LocationSerializerField()

    def get_moderatorOnlineList(self, obj):
        data = ModeratorOnlineScheduler.objects.filter(moderator_list__in=[obj])
        if len(data) > 0:
            return ModeratorOnlineSchedulerSerializer(data, many=True).data
        return []

    def get_owned_by(self, obj):
        data = obj.owned_by.all()
        if len(data) > 0:
            return UserSerializer(data, many=True).data
        return []

    def get_fake_users(self, obj):
        data = obj.fake_users.all()
        if len(data) > 0:
            return UserSerializer(data, many=True).data
        return []
    
    def get_stories(self,obj):
        stories_data = obj.story_set.all()
        if len(stories_data) < 0:
            return []
        reps = {}
        for each_story in stories_data:
            story_report_users = []
            for report_user in each_story.story_for_report.all():
                story_report_users.append(StoryReportSerializer(report_user).data)
            reps[f"{each_story.pk}"] = story_report_users
        return reps

    class Meta:
        model = User
        fields = [
            "books",
            "avatar_photos",
            # "owned_by",
            "is_fake",
            "sign_up",
            "created_at",
            "reports",
            "display_name",
            "id",
            "email",
            "twitter",
            "first_name",
            "last_name",
            "fullName",
            "gender",
            "about",
            "location",
            "isOnline",
            "familyPlans",
            "tags",
            "politics",
            "coins",
            "zodiacSign",
            "interestedIn",
            "interested_in",
            "ethnicity",
            "religion",
            "blockedUsers",
            "education",
            "music",
            "height",
            "age",
            "language",
            "language_id_code",
            "address",
            "moderatorOnlineList",
            "tvShows",
            "sportsTeams",
            # "sportsTeam",
            "movies",
            "work",
            "is_blocked",
            "username",
            "owner_id",
            "fake_users",
            "roles",
            "country",
            "country_code",
            "avatar_index",
            "city",
            "user_last_seen",
            "is_active",
            "subscription",
            "subscription_id",
            "is_active",
            "User_for_story_report",
            "stories",
            "User_for_report",
            "zip_code"
        ]
        extra_kwargs = {
            "owner_id": {"write_only": True},
        }
        read_only_fields = [
            "fake_users",
            # "owned_by"
        ]
        depth = 1
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['language_id_code'] = instance.get_language_id_code()
        return data

    def create(self, validated_data):
        owner_id = validated_data.pop("owner_id", "")
        books = validated_data.pop("book", "")
        movies = validated_data.pop("movies", "")
        music = validated_data.pop("music", "")
        sports_teams = validated_data.pop("sportsTeams", "")
        tags = validated_data.pop("tags", "")
        tv_shows = validated_data.pop("tvShows", "")
        language = validated_data.pop("language", "")
        subscription_id = validated_data.pop("subscription_id", None)
        moderatorOnlineList_id = validated_data.pop("moderatorOnlineList_id", "")
        fakeid = uuid.uuid4()
        fakeid = "bb2bb0" + str(fakeid)[6:]

        if "location" in validated_data:
            country, country_code, state, city, zip_code = get_country_from_geo_point(
                geo_point=validated_data["location"]
            )
            validated_data["country"] = country
            validated_data["country_code"] = country_code
            if not validated_data.get("zip_code"):
                validated_data["zip_code"] = zip_code

        user = User.objects.create(id=fakeid, **validated_data)
        user.book.set(books)
        user.movies.set(movies)
        user.music.set(music)
        user.sportsTeams.set(sports_teams)
        user.tags.set(tags)
        user.language.set(language)
        user.tvShows.set(tv_shows)
        # add subscriptions for moderator
        if user.is_fake and subscription_id:
            ModeratorSubscriptionPlan.objects.create(moderator=user, subscription_id=subscription_id)

        # moderatorOnlineList.moderator_list.add(user)
        # print(moderatorOnlineList)
        if moderatorOnlineList_id != "":
            m_list = ModeratorOnlineScheduler.objects.filter(id=moderatorOnlineList_id)
            if m_list.count():
                m_list[0].moderator_list.add(user)

        worker = User.objects.filter(id=owner_id)
        if worker.count():
            worker = worker[0]
            user.owned_by.add(worker)
            user.roles.add(UserRole.objects.get(role=UserRole.ROLE_FAKE_USER))
            user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # Add any custom update logic here
        if "language" in validated_data:
            language = validated_data["language"]
            lg_code = ""
            # print(user.language.all())
            for lng in language:
                lg_code += (lng.language_code).upper() + "-"
            print("user update", validated_data["language"])

            fields = [
                "books",
                "music",
            ]
            if instance.worker_id_code == 0:
                last_worker = User.objects.filter(
                    roles__role__in=["CHATTER"], worker_id_code__gt=0
                ).order_by("worker_id_code")
                if last_worker.count() == 0:
                    instance.worker_id_code = 1
                else:
                    instance.worker_id_code = last_worker.last().worker_id_code + 1

            instance.language_id_code = f"{lg_code}{instance.worker_id_code:07n}"

        if "location" in validated_data:
            country, country_code, state, city, zip_code = get_country_from_geo_point(
                geo_point=validated_data["location"]
            )
            instance.country = validated_data["country"] = country
            instance.country_code = validated_data["country_code"] = country_code
            instance.state = validated_data["state"] = state
            instance.city = validated_data["city"] = city
            instance.zip_code = validated_data["zip_code"] = zip_code
        # instance.isOnline = True
        # instance.user_last_seen = timezone.now()
        instance.save()
        return instance


class SignUpRequestSerialzier(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    invitation_key = serializers.UUIDField()
    password = serializers.CharField()
    paste_access = serializers.BooleanField()
    # allow_manual_chat = serializers.BooleanField()
