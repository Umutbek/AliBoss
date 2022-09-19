from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics, authentication
from django.shortcuts import redirect
from category import models, serializers, filters
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet
from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from django_filters import DateFilter
import requests


class StoreCategoryViewSet(viewsets.ModelViewSet):
    """Manage Store Category"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.StoreCategory.objects.all()
    serializer_class = serializers.StoreCategorySerializer
    pagination_class = None


class StoreViewSet(viewsets.ModelViewSet):
    """Manage Store"""
    permission_classes = (permissions.AllowAny,)
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.StoreFilter

    ordering_fields = ('priority',)

    search_fields = ('name', 'description', 'slogan')

    pagination_class = None


class RegularAccountViewSet(viewsets.ModelViewSet):
    """Manage Regular Accounts"""
    permission_classes = (permissions.AllowAny,)
    queryset = models.RegularAccount.objects.all()
    serializer_class = serializers.RegularAccountSerializer
    pagination_class = None


class GetMeView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class LoginAPI(APIView):
    """Create a new auth token for user"""
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        info = models.Store.objects.filter(login=user)
        userdata = serializers.StoreSerializer(info, many=True)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, 'data': userdata.data}, status=200)


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage Category"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    ordering = ('id', 'priority')
    ordering_fields = ('id', 'priority')

    filter_backends = (DjangoFilterBackend,SearchFilter, OrderingFilter)
    filter_class = filters.CategoryFilter
    pagination_class = None


class SubCategoryViewSet(viewsets.ModelViewSet):
    """Manage Store category"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.SubCategoryFilter
    pagination_class = None


class SubSubCategoryViewSet(viewsets.ModelViewSet):
    """Manage SubSubcategory"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.SubSubCategory.objects.all()
    serializer_class = serializers.SubSubCategorySerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.SubSubCategoryFilter
    pagination_class = None
