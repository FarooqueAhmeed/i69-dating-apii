from django.urls import path
from subscriptions import views

urlpatterns = [
    path("", views.SubscriptionPlanAPIView.as_view(), name="subscription_plans"),
    path("subscription_plans/", views.SubscriptionPlanAPIView.as_view(), name="subscription_plans"),
]