from django.db.models.base import ModelState
from rest_framework import fields, serializers
from defaultPicker import models
from user.models import ModeratorOnlineScheduler


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.age
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):

    country_flag = serializers.SerializerMethodField()

    def get_country_flag(self, obj):
        request = self.context.get("request")
        flag_url = None
        if obj.country_code:
            flag_url = request.build_absolute_uri(
                f"/static/img/country-flags/png250/{obj.country_code.lower()}.png"
            )
        return flag_url

    class Meta:
        model = models.Language
        fields = "__all__"


class HeightSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.height
        fields = "__all__"


class GenderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.gender
        fields = "__all__"


class SearchGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.searchGender
        fields = "__all__"


class EthnicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ethnicity
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.family
        fields = "__all__"


class PoliticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.politics
        fields = "__all__"


class ReligiousSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.religious
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tags
        fields = "__all__"


class ZodiacSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.zodiacSign
        fields = "__all__"


class InterestedInSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.interestedIn
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.config
        fields = "__all__"


class TvShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tvShows
        fields = "__all__"


class SportsTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.sportsTeams
        fields = "__all__"


class MoviesSerialzier(serializers.ModelSerializer):
    class Meta:
        model = models.movies
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.book
        fields = "__all__"


class ModeratorOnlineSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorOnlineScheduler
        fields = [
            "id",
            "list_name",
            "online_time",
            "offline_time",
        ]
