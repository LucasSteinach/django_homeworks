import django_filters.rest_framework

from .models import Stock


class StockFilter(django_filters.rest_framework.FilterSet):
    products = django_filters.rest_framework.DjangoFilterBackend()

    class Meta:
        model = Stock
        fields = ['products']
