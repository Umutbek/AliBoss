from rest_framework import serializers
from category import models
from django.contrib.auth import get_user_model, authenticate, password_validation
from django_filters import rest_framework as filters

from category.models import ModelAgent

User = get_user_model()
from rest_framework.authtoken.models import Token


class StoreCategorySerializer(serializers.ModelSerializer):
    """Serializer for store category"""

    class Meta:
        model = models.StoreCategory
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'icon')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user"""

    class Meta:
        model = User
        fields = ('id', 'name', 'login', 'phone', 'address', 'avatar')


class ModelAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelAgent
        fields = '__all__'


class ModelAgentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModelAgent
        fields = ('login', 'pin')


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for stores"""
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.Store
        fields = ('id', 'name', 'login', 'phone', 'avatar', 'email', 'address', 'location', 'longitude', 'latitude',
                  'instagram', 'facebook', 'whatsapp', 'web', 'slogan', 'description', 'rating', 'storecategory',
                  'priority', 'sale_type', 'visibility')

    def get_avatar(self, store):
        request = self.context.get('request')
        avatar = store.avatar.url
        return request.build_absolute_uri(avatar)


class Storeserializer(serializers.ModelSerializer):
    """Serializer for stores"""
    class Meta:
        model = models.Store
        fields = ('id', 'name', 'login', 'phone', 'email', 'address', 'location', 'longitude', 'latitude',
                  'instagram', 'facebook', 'whatsapp', 'web', 'slogan', 'description', 'rating', 'storecategory',
                  'priority', 'sale_type', 'visibility')


class RegularAccountSerializer(serializers.ModelSerializer):
    """Serializer for regular account"""

    class Meta:
        model = models.RegularAccount
        fields = ('id', 'name', 'login', 'phone', 'bonus', 'address',
                  'uid', 'magazin', 'isoptovik', 'optovik_start_date', 'optovik_end_date', 'password')

        extra_kwargs = {'password':{'write_only':True},}

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = models.RegularAccount.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login"""
    login = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type':'password'}, trim_whitespace=False
    )

    class Meta:
        model: User
        fields = ('login', 'password')

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        if login is None:
            raise serializers.ValidationError(
                'A phone or email is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(
            request = self.context.get('request'),
            login=login,
            password=password,
        )

        if not user:
            msg = ('Неправильный логин или пароль')
            raise serializers.ValidationError({'detail': msg}, code='authorization')

        data['user']= user

        return data


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category"""
    id = serializers.IntegerField()

    class Meta:
        model = models.Category
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'icon', 'store', 'isoptovik', 'priority')


class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for subcategory"""
    id = serializers.IntegerField()

    class Meta:
        model = models.SubCategory
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'category')


class SubSubCategorySerializer(serializers.ModelSerializer):
    """Serializer for subsubcategory"""
    id = serializers.IntegerField()

    class Meta:
        model = models.SubSubCategory
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'subcategory')


class ModelAgentHistorySerializer(serializers.ModelSerializer):
    user = RegularAccountSerializer()

    class Meta:
        model = models.ModelAgentHistory
        fields = ('agent', 'user', 'date', 'description')
