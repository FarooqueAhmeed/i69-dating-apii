import graphene
from graphene_django import DjangoObjectType

from .models import Package, PackagePermissionLimit, Permission, Plan, PlanForRegion
from defaultPicker.utils import translated_field_name


class PlanType(DjangoObjectType):
    id = graphene.Int()
    price_in_coins = graphene.Int()

    class Meta:
        model = Plan
        fields = "__all__"

    def resolve_price_in_coins(self, info):
        price_in_coins = self.price_in_coins
        user_region = info.context.user.get_coinsettings_region()
        if user_region:                    
            plan_for_region = PlanForRegion.objects.filter(plan=self, region=user_region, is_active=True).first()
            if plan_for_region:
                price_in_coins = plan_for_region.price_in_coins
        return price_in_coins

    def resolve_title(self, info):
        return getattr(self, translated_field_name(info.context.user, "title"))


class PackagePermissionLimitType(DjangoObjectType):
    class Meta:
        model = PackagePermissionLimit
        fields = "__all__"


class PermissionType(DjangoObjectType):
    packagepermissionlimit = graphene.List(PackagePermissionLimitType)

    class Meta:
        model = Permission
        fields = "__all__"

    def resolve_description(self, info):
        return getattr(self, translated_field_name(info.context.user, "description"))


class PackageType(DjangoObjectType):
    id = graphene.Int()
    plans = graphene.List(PlanType)
    permissions = graphene.List(PermissionType)

    class Meta:
        model = Package
        fields = "__all__"

    def resolve_plans(self, info):
        return Plan.objects.filter(package=self, is_active=True).order_by("id").all()

    def resolve_permissions(self, info):
        return Permission.objects.filter(package=self).all()

    def resolve_name(self, info):
        return getattr(self, translated_field_name(info.context.user, "name"))


class PurchaseCoinResponseType(graphene.ObjectType):
    id = graphene.Int()
    coins = graphene.Int()
    success = graphene.Boolean()


class UserSubscriptionType(graphene.ObjectType):
    package = graphene.Field(PackageType)
    plan = graphene.Field(PlanType)
    is_active = graphene.Boolean()
    starts_at = graphene.DateTime()
    ends_at = graphene.DateTime()
    is_cancelled = graphene.Boolean()
    cancelled_at = graphene.DateTime()
