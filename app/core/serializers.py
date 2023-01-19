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
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory', 'cost', 'costSale', 'issale',
            'supplier', 'uniqueid', 'image', 'phone', 'instagram', 'facebook', 'whatsapp', 'web',
            'likes', 'views', 'imagelink', 'sale_type', 'isoptovik', 'optovikcost', 'priority'
            )

        read_only_fields = ('id',)


class GetItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'category', 'subcategory', 'subsubcategory',
            'cost', 'costSale', 'issale', 'supplier', 'uniqueid', 'image', 'phone',
            'imagelink', 'instagram', 'facebook', 'whatsapp', 'web', 'likes', 'views', 'isoptovik',
            'optovikcost', 'priority'
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


class CartItemSerializerGet(serializers.ModelSerializer):
    """Serializer for cart items"""
    item = GetItemSerializer()

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
            'comment', 'storeName', 'storeLogo', 'status', 'date', 'isoptovik', 'bonus', 'pay_status', 'user_id'
        )
        read_only_fields = ('id',)


    def create(self, validated_data):

        items = validated_data.pop("items", None)
        order = models.ModelOrder.objects.create(**validated_data)

        if items:
            for i in items:
                models.CartItems.objects.create(order=order, **i)
        return order


class ClientOrderSerializerGet(serializers.ModelSerializer):
    """Serializer for client order"""
    items = CartItemSerializerGet(many=True, required=False, allow_null=True)

    class Meta:
        model = models.ModelOrder
        fields = (
            'id', 'items', "store", "totalCost", "user", 'address', 'phone', 'lat', 'lon',
            'comment', 'storeName', 'storeLogo', 'status', 'date', 'isoptovik', 'bonus', 'pay_status', 'user_id'
        )
        read_only_fields = ('id',)


    def create(self, validated_data):

        items = validated_data.pop("items", None)
        order = models.ModelOrder.objects.create(**validated_data)

        if items:
            for i in items:
                models.CartItems.objects.create(order=order, **i)
        return order


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = '__all__'


class ServiceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceSubCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Services"""

    class Meta:
        model = models.Services
        fields = (
            'id', 'name', 'description', 'cost', 'costSale', 'issale', 'services_category', 'services_sub_category',
            'supplier', 'image', 'phone', 'instagram', 'facebook', 'whatsapp', 'web',
            'likes', 'views', 'imagelink', 'priority'
            )

        read_only_fields = ('id',)


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner"""

    class Meta:
        model = models.Banner
        fields = (
            'id', 'photo', 'link', 'color', 'isoptovik'
            )

        read_only_fields = ('id',)


class BonusHistorySerializer(serializers.ModelSerializer):
    order = ClientOrderSerializer()

    class Meta:
        model = models.BonusHistory
        fields = ('date', 'amount', 'user', 'order', 'description')


class AddBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegularAccount
        fields = ('user', 'bonus')
