from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    creator = filters.NumberFilter(
        label="creator",
        field_name="creator"
    )
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ["creator", "created_at"]
