from rest_framework import serializers
from .models import ModeratorSubscriptionPlan

class SubscriptionPlanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)



class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorSubscriptionPlan
        fields=["id", "name", "user"]