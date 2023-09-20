import graphene
from django.utils import timezone
from django.db.models import Q

from moments.models import Moment
from user.models import User

from .decorators import check_permission, login_required
from .models import Package, PackagePurchase, Plan, Purchase, PlanForRegion
from payments.models import BokuPayment, Charge, PayPalOrder, StripeIntent, SetAllowedPaymentMethods, PaymentGatewayForRegion
from .types import PurchaseCoinResponseType
from .utils import package_plans_duration_timedeltas
from .tasks import check_package_task
from user.utils import translate_error_message


class PurchaseCoinMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        method = graphene.String()
        coins = graphene.Int()
        money = graphene.Float()
        payment_method = graphene.String()
        currency = graphene.String(required=True)
        payment_id = graphene.String()

    Output = PurchaseCoinResponseType

    def mutate(
        self,
        info,
        id,
        coins,
        money,
        payment_method,
        payment_id,
        currency,
        method="COINS",
    ):
        user = User.objects.get(id=id)
        payment_gateways = (PaymentGatewayForRegion.objects.filter(
            Q(region__countries__name__iexact=user.country_code), Q(is_allowed=True)
        ))
        payment_gateways = payment_gateways.values('payment_gateway__payment_method')

        if not [
            pay_method["payment_gateway__payment_method"] for pay_method in payment_gateways
            if pay_method["payment_gateway__payment_method"].lower() == payment_method.lower()
        ]:
            raise Exception(translate_error_message(info.context.user, "Provided payment Method is invalid."))

        # verify the provided purchase_id
        payment_verified = False
        try:
            if payment_method.lower() == "boku":
                boku_payment = BokuPayment.objects.get(charging_token=payment_id)
                boku_charge = Charge.objects.get(payment=boku_payment)
                if (
                    float(boku_charge.price) == money
                    and boku_charge.transaction_state == "charged"
                ):
                    payment_verified = True
            elif payment_method.lower() == "paypal":
                paypal_order = PayPalOrder.objects.get(order_id=payment_id)
                if (
                    float(paypal_order.amount) == money
                    and paypal_order.status == "COMPLETED"
                ):
                    payment_verified = True
            elif payment_method.lower() == "stripe":
                stripe_intent = StripeIntent.objects.get(intent_id=payment_id)
                if (
                    float(stripe_intent.amount) == money
                    and stripe_intent.status == "succeeded"
                ):
                    payment_verified = True
            else:
                payment_verified = True
        except Exception:
            raise Exception(translate_error_message(info.context.user, "Provided payment ID is invalid."))

        if not payment_verified:
            raise Exception(translate_error_message(info.context.user, "Unable to verify payment status for the purchased coins."))

        new_purchase = Purchase.objects.create(
            user=user,
            method=method,
            coins=coins,
            money=money,
            payment_method=payment_method,
            currency=currency,
        )
        # new_purchase.save()

        return PurchaseCoinResponseType(
            id=new_purchase.purchase_id, coins=user.coins, success=True
        )


class PurchasePackageMutation(graphene.Mutation):
    class Arguments:
        package_id = graphene.Int(required=True)
        plan_id = graphene.Int(required=True)

    id = graphene.Int()
    success = graphene.Boolean()

    def mutate(self, info, package_id, plan_id):
        user = info.context.user
        package = Package.objects.get(id=package_id)

        try:
            plan = Plan.objects.get(id=plan_id, package_id=package_id)
        except Plan.DoesNotExist:
            raise Exception(translate_error_message(info.context.user, "Plan does not exists."))

        now = timezone.now()
        starts_at = now
        ends_at = now + package_plans_duration_timedeltas.get(plan.validity)

        if ends_at < now:
            raise Exception(translate_error_message(info.context.user, "Plan end date is passed please choose a valid plan type"))

        existing_memebership = PackagePurchase.objects.filter(
            user=user, is_active=True, starts_at__lte=now, ends_at__gte=now
        ).first()

        if existing_memebership:
            raise Exception(translate_error_message(info.context.user, "Active package already found for this user."))

        # get price based on user's region
        user_region = user.get_coinsettings_region()
        if user_region:                    
            plan_for_region = PlanForRegion.objects.filter(plan=plan, region=user_region, is_active=True).first()
            if plan_for_region:
                plan.price_in_coins = plan_for_region.price_in_coins

        user.deductCoins(plan.price_in_coins, "Package purchase")
        user.save()

        purchase_package = PackagePurchase.objects.create(
            user=user,
            package=package,
            plan=plan,
            package_price=plan.price_in_coins,
            purchase_price=plan.price_in_coins,
            starts_at=starts_at,
            ends_at=ends_at,
            is_active=True,
        )

        return PurchasePackageMutation(id=purchase_package.id, success=True)


class UpgradePackageMutation(graphene.Mutation):
    class Arguments:
        new_package_id = graphene.Int(required=True)
        # plan_id = graphene.Int(required=True)

    id = graphene.Int()
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, new_package_id):
        user = info.context.user
        now = timezone.now()
        subscription = PackagePurchase.objects.filter(
            user=info.context.user, is_active=True, starts_at__lte=now, ends_at__gte=now
        ).first()

        if not subscription:
            raise Exception(translate_error_message(info.context.user, "You have not subscribed to any package."))

        # Calculate the upgrade price
        remaining = 100 - (
            timezone.now().timestamp() - subscription.starts_at.timestamp()
        ) / (subscription.ends_at.timestamp() - subscription.starts_at.timestamp())
        remaining = round(remaining, 2)

        if subscription.package.id == new_package_id:
            raise Exception(
                translate_error_message(info.context.user, "You are currently on the same package, Please choose an other package.")
            )

        if subscription.package.id > new_package_id:
            raise Exception(translate_error_message(info.context.user, "Please chhose valid package to upgrade."))

        plan = Plan.objects.filter(
            package_id=new_package_id, title=subscription.plan.title
        ).first()
        starts_at = subscription.starts_at
        ends_at = starts_at + package_plans_duration_timedeltas.get(plan.validity)

        if ends_at < now:
            raise Exception(translate_error_message(info.context.user, "Plan end date is passed please choose a valid plan type"))

        coins_needed = int(remaining * plan.price_in_coins)
        user.deductCoins(coins_needed, "Package upgrade")
        user.save()

        upgraded = PackagePurchase.objects.create(
            user=info.context.user,
            plan_id=plan.id,
            package_id=new_package_id,
            starts_at=starts_at,
            ends_at=ends_at,
            package_price=coins_needed,
            purchase_price=coins_needed,
            is_active=True,
        )

        PackagePurchase.objects.filter(id=subscription.id).update(
            upgraded_at=timezone.now(),
            upgraded_to_package=upgraded.package,
            is_active=False,
        )

        return UpgradePackageMutation(
            id=upgraded.id, message=f"Package upgrade successfull.", success=True
        )


class DowngradePackageMutation(graphene.Mutation):
    class Arguments:
        new_package_id = graphene.Int(required=True)

    id = graphene.Int()
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, new_package_id):
        now = timezone.now()
        subscription = PackagePurchase.objects.filter(
            user=info.context.user, is_active=True, starts_at__lte=now, ends_at__gte=now
        ).first()

        if not subscription:
            raise Exception(translate_error_message(info.context.user, "You have not subscribed to any package."))

        if subscription.package.id == new_package_id:
            raise Exception(
                translate_error_message(info.context.user, "You are currently on the same package, Please choose an other package.")
            )

        if subscription.package.id < new_package_id:
            raise Exception(translate_error_message(info.context.user, "Please chose valid package to downgrade."))

        PackagePurchase.objects.filter(pk=subscription.pk).update(
            downgraded_at=timezone.now(),
            downgraded_to_package_id=new_package_id,
        )

        return DowngradePackageMutation(
            id=new_package_id, message=translate_error_message(info.context.user, f"Package downgrade successfull."), success=True
        )


class CancelSubscriptionMutation(graphene.Mutation):

    message = graphene.String()
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        now = timezone.now()

        subscription = PackagePurchase.objects.filter(
            user=info.context.user, is_active=True, starts_at__lte=now, ends_at__gte=now
        ).first()

        if not subscription:
            raise Exception(translate_error_message(info.context.user, "You have not subscribed to any package."))

        PackagePurchase.objects.filter(id=subscription.id).update(cancelled_at=now)

        return CancelSubscriptionMutation(
            message=translate_error_message(info.context.user, "Subscription cancelled successfully."), success=True
        )


class PermissionTestMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    name = graphene.String()
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, name):

        check_package_task.apply_async(args=[info.context.user.username])
        qs = Moment.objects.filter(user=info.context.user)

        check_permission(
            user=info.context.user,
            permission="SHARE_STORY",
            date_field="created_date",
            qs=qs,
        )

        return PermissionTestMutation(
            name=name,
            message=translate_error_message(info.context.user, "Story Shared successfly"),
            success=True,
        )
