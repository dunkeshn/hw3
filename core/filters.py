import django_filters
from core import models
from django.db.models import Q

class Order(django_filters.FilterSet):

    price_range = django_filters.RangeFilter(field_name='deliveries__sum', label='Цена от и до')
    address = django_filters.CharFilter(lookup_expr='icontains', label='Адрес')
    received = django_filters.BooleanFilter(method='filter_received', label='Заказ получен')
    term = django_filters.CharFilter(method='filter_term', label='')
    content = django_filters.CharFilter(method='filter_content', label='Содержание заказа')

    class Meta:
        model = models.Order
        fields = ['term']

    def filter_received(self, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(deliveries__amount__gt=0)
        return queryset.filter(deliveries__amount=0)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(address__icontains=term) | Q(sum__icontains=term)
        return queryset.filter(criteria).distinct()

    def filter_content(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(products__name__icontains=term) | Q(products__description__icontains=term)
        return queryset.filter(criteria).distinct()