from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()

    # TODO: задайте требуемые фильтры

    class Meta:
        model = Advertisement
        fields = ['id', 'creator', 'status', 'created_at',]
