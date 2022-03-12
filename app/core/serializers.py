from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model, authenticate, password_validation
from django_filters import rest_framework as filters
User = get_user_model()
from rest_framework.authtoken.models import Token


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory', 'cost',
            'supplier', 'uniqueid', 'image', 'phone', 'instagram', 'facebook', 'whatsapp', 'web',
            'likes', 'views', 'imagelink'
            )

        read_only_fields = ('id',)


class GetItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory', 'cost',
            'supplier', 'uniqueid', 'image', 'phone', 'imagelink'
            )

        read_only_fields = ('id',)
        depth=1


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    class Meta:
        model = models.CartItems
        fields = (
            'id', 'item', 'quantity'
        )
        read_only_fields = ('id',)


class ClientOrderSerializer(serializers.ModelSerializer):
    """Serializer for client order"""
    items = CartItemSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.ModelOrder
        fields = (
            'id', 'items', "store", "totalCost", "user", 'address', 'phone', 'lat', 'lon',
            'comment', 'storeName', 'storeLogo', 'status', 'date',
        )
        read_only_fields = ('id',)


    def create(self, validated_data):

        items = validated_data.pop("items", None)
        order = models.ModelOrder.objects.create(**validated_data)

        if items:
            for i in items:
                models.CartItems.objects.create(order=order, **i)
        return order