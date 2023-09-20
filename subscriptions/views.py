from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (
    SubscriptionsPlan
)
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer


class SubscriptionPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subscription_plan = SubscriptionsPlan.objects.all()
            serializers = SubscriptionPlanSerializer(subscription_plan, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except SubscriptionsPlan.DoesNotExist:
            content = {"error": "subscription objects is not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
