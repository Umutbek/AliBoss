from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from core.models import User
from core import models
from django.db.models import Q


class ItemFilter(FilterSet):
    """Filter for an item"""
    category = filters.CharFilter('category')
    subcategory = filters.CharFilter('subcategory')
    subsubcategory = filters.CharFilter('subsubcategory')

    supplier = filters.CharFilter('supplier')
    uniqueid = filters.CharFilter('uniqueid')
    issale = filters.CharFilter('issale')
    isoptovik = filters.CharFilter('isoptovik')

    min_cost= filters.CharFilter(field_name="cost",lookup_expr='gte')
    max_cost= filters.CharFilter(field_name="cost",lookup_expr='lte')

    class Meta:
        models = models.Item
        fields = ('uniqueid', 'category', 'subcategory', 'subsubcategory', 'min_cost', 'max_cost', 'min_cost',
                  'isoptovik', 'issale', 'supplier')


class OrderFilter(FilterSet):
    """Filter for an order"""
    store = filters.CharFilter('store')
    isoptovik = filters.CharFilter('isoptovik')
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        models = models.ModelOrder
        fields = ('store', 'start_date', 'end_date', 'isoptovik')


class BannerFilter(FilterSet):
    """Filter for banners"""
    isoptovik = filters.CharFilter('isoptovik')

    class Meta:
        models = models.Banner
        fields = ('isoptovik',)