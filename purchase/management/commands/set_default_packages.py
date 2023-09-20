from django.core.management.base import BaseCommand

from purchase.models import Package, Plan


class Command(BaseCommand):
    def handle(self, *args, **options):
        default_packages = {
            "packages": [
                {
                    "name": "SILVER  PACKAGE",
                    "description": "some services",
                    "plan": [
                        {
                            "title": "PER WEEK",
                            "validity": "PERWEEK",
                            "price_in_coins": 5,
                        },
                        {
                            "title": "PER MONTH",
                            "validity": "PERMONTH",
                            "price_in_coins": 10,
                        },
                        {
                            "title": "PER 3 MONTH",
                            "validity": "PER3MONTH",
                            "price_in_coins": 25,
                        },
                        {
                            "title": "PER 6 MONTH",
                            "validity": "PER6MONTH",
                            "price_in_coins": 60,
                        },
                        {
                            "title": "PER YEAR",
                            "validity": "PERYEAR",
                            "price_in_coins": 100,
                        },
                    ],
                },
                {
                    "name": "GOLD PACKAGE",
                    "description": "more services",
                    "plan": [
                        {
                            "title": "PER WEEK",
                            "validity": "PERWEEK",
                            "price_in_coins": 5,
                        },
                        {
                            "title": "PER MONTH",
                            "validity": "PERMONTH",
                            "price_in_coins": 10,
                        },
                        {
                            "title": "PER 3 MONTH",
                            "validity": "PER3MONTH",
                            "price_in_coins": 25,
                        },
                        {
                            "title": "PER 6 MONTH",
                            "validity": "PER6MONTH",
                            "price_in_coins": 60,
                        },
                        {
                            "title": "PER YEAR",
                            "validity": "PERYEAR",
                            "price_in_coins": 100,
                        },
                    ],
                },
                {
                    "name": "PLATINUM PACKAGE",
                    "description": "will full services",
                    "plan": [
                        {
                            "title": "PER WEEK",
                            "validity": "PERWEEK",
                            "price_in_coins": 5,
                        },
                        {
                            "title": "PER MONTH",
                            "validity": "PERMONTH",
                            "price_in_coins": 10,
                        },
                        {
                            "title": "PER 3 MONTH",
                            "validity": "PER3MONTH",
                            "price_in_coins": 25,
                        },
                        {
                            "title": "PER 6 MONTH",
                            "validity": "PER6MONTH",
                            "price_in_coins": 60,
                        },
                        {
                            "title": "PER YEAR",
                            "validity": "PERYEAR",
                            "price_in_coins": 100,
                        },
                    ],
                },
            ]
        }

        for package_ in default_packages["packages"]:
            pack = Package.objects.get_or_create(
                name=package_["name"],
                description=package_["description"],
                defaults={
                    "name": package_["name"],
                    "description": package_["description"],
                },
            )[0]
            for plan_ in package_["plan"]:
                Plan.objects.get_or_create(
                    package=pack,
                    title=plan_["title"],
                    validity=plan_["validity"],
                    defaults={
                        "title": plan_["title"],
                        "validity": plan_["validity"],
                        "price_in_coins": plan_["price_in_coins"],
                        "package": pack,
                    },
                )
