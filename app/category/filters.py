from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from category import models
from django.db.models import Q


class CategoryFilter(FilterSet):
    """Filter for a category"""
    store = filters.CharFilter('store')

    class Meta:
        models = models.Category
        fields = ('store',)


class SubCategoryFilter(FilterSet):
    """Filter for a subcategory"""
    category = filters.CharFilter('category')

    class Meta:
        models = models.SubCategory
        fields = ('category',)


class SubSubCategoryFilter(FilterSet):
    """Filter for a subsubcategory"""
    subcategory = filters.CharFilter('subcategory')

    class Meta:
        models = models.SubSubCategory
        fields = ('subcategory',)