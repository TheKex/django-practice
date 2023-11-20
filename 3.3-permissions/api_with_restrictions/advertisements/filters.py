from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    creator = filters.NumberFilter(
        label="creator",
        field_name="creator"
    )
    created_at = filters.DateFromToRangeFilter()

    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)

    class Meta:
        model = Advertisement
        fields = ["creator", "created_at", "status"]
