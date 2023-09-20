import django_filters
from user.models import User


class UserFilter(django_filters.FilterSet):
    age_from = django_filters.NumberFilter(field_name="age", lookup_expr="gte")
    age_to = django_filters.NumberFilter(field_name="age", lookup_expr="lte")
    gender = django_filters.NumberFilter(field_name="gender")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
    last_seen_from = django_filters.DateTimeFilter(field_name="user_last_seen", lookup_expr="gte")
    last_seen_to = django_filters.DateTimeFilter(field_name="user_last_seen", lookup_expr="lte")
    last_seen_hour = django_filters.NumberFilter(field_name="user_last_seen", method="filter_last_seen_hour")
    last_seen_day = django_filters.NumberFilter(field_name="user_last_seen", method="filter_last_seen_day")
    join_date_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    join_date_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    join_date_hour = django_filters.NumberFilter(field_name="created_at", method="filter_join_date_hour")
    join_date_day = django_filters.NumberFilter(field_name="created_at", method="filter_join_date_day")
    s_online = django_filters.BooleanFilter(field_name="isOnline")

    class Meta:
        model = User
        fields = []

    def filter_last_seen_hour(self, queryset, name, value):
        return queryset.filter(user_last_seen__hour=int(value))

    def filter_last_seen_day(self, queryset, name, value):
        return queryset.filter(user_last_seen__day=int(value))

    def filter_join_date_hour(self, queryset, name, value):
        return queryset.filter(created_at__hour=int(value))

    def filter_join_date_day(self, queryset, name, value):
        return queryset.filter(created_at__day=int(value))

class ModeratorFilter(django_filters.FilterSet):
    age_from = django_filters.NumberFilter(field_name="age", lookup_expr="gte")
    age_to = django_filters.NumberFilter(field_name="age", lookup_expr="lte")
    gender = django_filters.NumberFilter(field_name="gender")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")

    class Meta:
        model = User
        fields = []


class WorkerFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name="id", lookup_expr="icontains")
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = User
        fields = []
