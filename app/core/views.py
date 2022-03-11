from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect
from core import models, serializers, filters
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from django_filters import DateFilter
import requests


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage Category"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    filter_backends = (DjangoFilterBackend,)
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


class ItemViewSet(viewsets.ModelViewSet):
    """Manage item"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.ItemFilter

    ordering_fields = ('cost',)

    search_fields = ('name',)

    # def get_serializer_class(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return serializers.GetItemSerializer
    #     return serializers.ItemSerializer
