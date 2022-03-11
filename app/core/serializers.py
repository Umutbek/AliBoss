from rest_framework import serializers
from core import models
from django_filters import rest_framework as filters


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory', 'cost',
            'supplier', 'uniqueid', 'image', 'phone', 'instagram', 'facebook', 'whatsapp', 'web',
            'likes', 'views'
            )

        read_only_fields = ('id',)


class GetItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory', 'cost',
            'supplier', 'uniqueid', 'image', 'phone'
            )

        read_only_fields = ('id',)
        depth=1


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category"""
    class Meta:
        model = models.Category
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'icon', 'store')
        read_only_fields = ('id',)


class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for subcategory"""

    class Meta:
        model = models.SubCategory
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'category')


class SubSubCategorySerializer(serializers.ModelSerializer):
    """Serializer for subsubcategory"""

    class Meta:
        model = models.SubSubCategory
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'subcategory')
