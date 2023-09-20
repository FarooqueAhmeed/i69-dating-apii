from dateutil.relativedelta import relativedelta

payment_method_choices = [
    ("Gpay", "Gpay"),
    ("Stripe", "Stripe"),
    ("Boku", "Boku"),
    ("PayPal", "PayPal"),
]

package_plan_duration_choices = (
    ("PERWEEK", "PER WEEK"),
    ("PERMONTH", "PER MONTH"),
    ("PER3MONTH", "PER 3 MONTH"),
    ("PER6MONTH", "PER 6 MONTH"),
    ("PERYEAR", "PER YEAR"),
)

package_plans_duration_timedeltas = {
    "PERWEEK": relativedelta(weeks=+1),
    "PERMONTH": relativedelta(months=+1),
    "PER3MONTH": relativedelta(months=+3),
    "PER6MONTH": relativedelta(months=+6),
    "PERYEAR": relativedelta(years=+1),
}

cancel_subscription_choices = [
    ("Yes", "Yes"),
    ("No", "No"),
]
