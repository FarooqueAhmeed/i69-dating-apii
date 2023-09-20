from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Count

from .models import PackagePermissionLimit, PackagePurchase, Permission
from user.utils import translate_error_message


def has_permission(**check_args):
    def real_authorization_checker(wrapped_func):
        def wrapper(*args, **kwargs):
            now = timezone.now()
            subscription = PackagePurchase.objects.filter(
                user=args[1].context.user,
                is_active=True,
                starts_at__lte=now,
                ends_at__gte=now,
            ).first()

            if not subscription:
                raise Exception(
                    "You dont have permission to perform this action. Please upgrade you package."
                )

            permissions = [
                *Permission.objects.filter(package=subscription.package).values_list(
                    "name", flat=True
                )
            ]

            if not check_args["permission"] in permissions:
                raise Exception(
                    "You dont have permission to perform this action. Please upgrade you package."
                )

            return wrapped_func(*args, **kwargs)

        wrapper.__name__ = wrapped_func.__name__
        return wrapper

    return real_authorization_checker


def login_required(func):
    def wrapper(*args, **kwargs):
        user = args[1].context.user
        if user is None or not user.is_authenticated:
            raise Exception("You are not logged in")
        return func(*args, **kwargs)

    return wrapper


def check_permission(
    user, permission=None, date_field="created_date", qs=None, room=None
):

    now = timezone.now()
    subscription = PackagePurchase.objects.filter(
        user=user, is_active=True, starts_at__lte=now, ends_at__gte=now
    ).first()

    if not subscription:
        permissiion_object = Permission.objects.filter(name=permission).first()
        if permissiion_object:
            day_args = {
                f"{date_field}__year": now.year,
                f"{date_field}__month": now.month,
                f"{date_field}__day": now.day,
            }

            updated_qs = qs.filter(**day_args)

            same_user = None
            if permission == "FIRST_FREE_MESSAGE":
                day_count = (
                    updated_qs.values("room_id__target__email")
                    .annotate(count=Count("room_id__target"))
                    .order_by("room_id__target")
                    .distinct()
                    .count()
                )
                same_user = updated_qs.filter(room_id__target=room.target)
            else:
                day_count = updated_qs.count()

            free_limit = permissiion_object.user_free_limit
            if day_count >= free_limit and permission != "FIRST_FREE_MESSAGE":
                raise Exception(
                    translate_error_message(user, "You have reached your daily free limit. Please purchase a package for higher limits.")
                )
            elif (
                day_count >= free_limit or same_user
            ) and permission == "FIRST_FREE_MESSAGE":
                print("********STEP 1***********")
                return False
    else:
        permissions = [
            *Permission.objects.filter(package=subscription.package).values_list(
                "name", flat=True
            )
        ]
        if not permission in permissions and permission != "FIRST_FREE_MESSAGE":
            raise Exception(
                translate_error_message(user, "You dont have permission to perform this action. Please upgrade you package.")
            )
        elif not permission in permissions and permission == "FIRST_FREE_MESSAGE":
            day_args = {
                f"{date_field}__year": now.year,
                f"{date_field}__month": now.month,
                f"{date_field}__day": now.day,
            }

            updated_qs = qs.filter(**day_args)
            day_count = (
                updated_qs.values("room_id__target__email")
                .annotate(count=Count("room_id__target"))
                .order_by("room_id__target")
                .distinct()
                .count()
            )
            if day_count > 0:
                return False

        limit = PackagePermissionLimit.objects.filter(
            permission__name=permission, package=subscription.package
        ).first()

        if limit:
            limit_exceel_message = "You have reached the {} of {} for {}, Upgrade you package to get higher limits."
            if not limit.is_unlimited:
                now = timezone.now()
                last_week = now - relativedelta(weeks=1)
                last_month = now - relativedelta(months=1)

                day_args = {
                    f"{date_field}__year": now.year,
                    f"{date_field}__month": now.month,
                    f"{date_field}__day": now.day,
                }
                updated_qs = qs.filter(**day_args)
                same_user = None
                if permission == "FIRST_FREE_MESSAGE":
                    day_count = (
                        updated_qs.values("room_id__target__email")
                        .annotate(count=Count("room_id__target"))
                        .order_by("room_id__target")
                        .distinct()
                        .count()
                    )
                    same_user = updated_qs.filter(room_id__target=room.target)
                else:
                    day_count = updated_qs.count()

                if day_count >= limit.per_day and permission != "FIRST_FREE_MESSAGE":
                    limit_exceel_message.format("daily", limit.per_day, permission)
                    raise Exception(
                        translate_error_message(user, limit_exceel_message.format("daily", limit.per_day, permission))
                    )
                elif (
                    day_count >= limit.per_day or same_user
                ) and permission == "FIRST_FREE_MESSAGE":
                    print("********STEP 3***********")
                    return False

                week_args = {f"{date_field}__range": [last_week, now]}
                updated_qs = qs.filter(**week_args)
                same_user = None
                if permission == "FIRST_FREE_MESSAGE":
                    week_count = (
                        updated_qs.values("room_id__target__email")
                        .annotate(count=Count("room_id__target"))
                        .order_by("room_id__target")
                        .distinct()
                        .count()
                    )
                    same_user = updated_qs.filter(room_id__target=room.target)
                else:
                    week_count = updated_qs.count()

                if week_count >= limit.per_week and permission != "FIRST_FREE_MESSAGE":
                    raise Exception(
                        translate_error_message(user, limit_exceel_message.format(
                            "weekly", limit.per_week, permission
                        ))
                    )
                elif (
                    week_count >= limit.per_week or same_user
                ) and permission == "FIRST_FREE_MESSAGE":
                    print("********STEP 4***********")
                    return False

                month_args = {f"{date_field}__range": [last_month, now]}

                updated_qs = qs.filter(**month_args)
                same_user = None
                if permission == "FIRST_FREE_MESSAGE":
                    month_count = (
                        updated_qs.values("room_id__target__email")
                        .annotate(count=Count("room_id__target"))
                        .order_by("room_id__target")
                        .distinct()
                        .count()
                    )
                    same_user = updated_qs.filter(room_id__target=room.target)
                else:
                    month_count = updated_qs.count()

                if (
                    month_count >= limit.per_month
                    and permission != "FIRST_FREE_MESSAGE"
                ):
                    raise Exception(
                        translate_error_message(user, limit_exceel_message.format(
                            "monthly", limit.per_month, permission
                        ))
                    )
                elif (
                    month_count >= limit.per_month or same_user
                ) and permission == "FIRST_FREE_MESSAGE":
                    print("********STEP 5***********")
                    return False

    return True
