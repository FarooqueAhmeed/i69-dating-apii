import graphene
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene import relay
from .models import Package, PackagePurchase, CoinPrices, CoinPricesForRegion
from .mutations import (
    CancelSubscriptionMutation,
    DowngradePackageMutation,
    PermissionTestMutation,
    PurchaseCoinMutation,
    PurchasePackageMutation,
    UpgradePackageMutation,
)
from .types import PackageType, UserSubscriptionType


class GetCoinPrices(DjangoObjectType):
    class Meta:
        model = CoinPrices
        fields = "__all__"
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_packages = graphene.List(PackageType)
    user_subscription = graphene.Field(UserSubscriptionType)
    get_coin_prices = graphene.List(GetCoinPrices)

    def resolve_get_coin_prices(self, info):
        user = info.context.user
        user_region = user.get_coinsettings_region()
        if not user_region:
            coinprices = CoinPrices.objects.filter(is_active=True).order_by("coins_count")
        else:
            regional_prices = CoinPricesForRegion.objects.filter(
                region=user_region,
            ).order_by("coins_count").prefetch_related("coin_price")

            coinprices = []
            for price in regional_prices:
                price_ = price.coin_price
                for f in ['coins_count', 'original_price', 'discounted_price']:
                    setattr(price_, f, getattr(price, f))
                coinprices.append(price_)

        return coinprices

    def resolve_all_packages(self, info):
        return Package.objects.filter().all()

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

        return UserSubscriptionType(
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


class Mutation(graphene.ObjectType):
    purchase_coin = PurchaseCoinMutation.Field()
    purchase_package = PurchasePackageMutation.Field()
    upgrade_package = UpgradePackageMutation.Field()
    downgrade_package = DowngradePackageMutation.Field()
    cancel_membership = CancelSubscriptionMutation.Field()
    permission_test = PermissionTestMutation.Field()
