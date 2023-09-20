from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from defaultPicker import models, serializers
from user.models import ModeratorOnlineScheduler
from subscriptions import serializers as subscriptionSerializer, models as subscriptionModel
from django_countries import countries


class DefaultPickersView(APIView):
    permission_classes = ()

    def get(self, request):
        pickers = {}

        def get_all(key, serializer, model):
            pickers[key] = serializer(model.objects.all(), many=True, context={"request": request}).data

        if not request.user.is_authenticated:
            get_all("languages", serializers.LanguageSerializer, models.Language)
            get_all("subscriptions", subscriptionSerializer.SubscriptionPlanSerializer, subscriptionModel.SubscriptionsPlan)
            pickers["countries"] = []
            for code, name in dict(countries).items():
                pickers["countries"].append({
                    "code": code,
                    "name": name,
                    "flag_url": request.build_absolute_uri(f"/static/img/country-flags/png250/{code.lower()}.png")
                })
        else:
            get_all("ages", serializers.AgeSerializer, models.age)
            get_all("languages", serializers.LanguageSerializer, models.Language)
            get_all("ethnicity", serializers.EthnicitySerializer, models.ethnicity)
            get_all("family", serializers.FamilySerializer, models.family)
            get_all("genders", serializers.GenderSerilizer, models.gender)
            get_all("heights", serializers.HeightSerilizer, models.height)
            get_all("politics", serializers.PoliticsSerializer, models.politics)
            get_all("religious", serializers.ReligiousSerializer, models.religious)
            get_all(
                "searchGenders", serializers.SearchGenderSerializer, models.searchGender
            )
            get_all("tags", serializers.TagsSerializer, models.tags)
            get_all("zodiacSigns", serializers.ZodiacSignSerializer, models.zodiacSign)
            get_all(
                "moderatorOnlineLists",
                serializers.ModeratorOnlineSchedulerSerializer,
                ModeratorOnlineScheduler,
            )
            get_all("subscriptions", subscriptionSerializer.SubscriptionPlanSerializer, subscriptionModel.SubscriptionsPlan)
            pickers["countries"] = []
            for code, name in dict(countries).items():
                pickers["countries"].append({
                    "code": code,
                    "name": name,
                    "flag_url": request.build_absolute_uri(f"/static/img/country-flags/png250/{code.lower()}.png")
                })

        if not request.user.is_authenticated:
            response = {
                "detail": "Authentication credentials were not provided.",
                "defaultPickers": pickers
            }
        else:
            response = {
                "defaultPickers": pickers
            }

        return Response(response)


default_picker_view = DefaultPickersView.as_view()
