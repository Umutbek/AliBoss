from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect
from core import models, serializers, filters, functions
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet
from rest_framework.authtoken.models import Token

from django.db.models import Sum, Count, F, Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from django_filters import DateFilter
import requests


class ItemViewSet(viewsets.ModelViewSet):
    """Manage item"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.ItemFilter

    ordering_fields = ('cost', 'priority')

    search_fields = ('name',)

    def get_queryset(self):
        return self.queryset.all().order_by("-priority", '-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.GetItemSerializer
        return serializers.ItemSerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.AllowAny,)
    queryset = models.ServiceCategory.objects.all()
    serializer_class = serializers.ServiceCategorySerializer


class ServiceSubCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.ServiceSubCategory.objects.all()
    serializer_class = serializers.ServiceSubCategorySerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """Manage services"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Services.objects.all()
    serializer_class = serializers.ServiceSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.ServiceFilter
    ordering_fields = ('cost', 'priority', 'category')

    search_fields = ('name',)


class BannerViewSet(viewsets.ModelViewSet):
    """Manage banners"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.BannerFilter


class OrderViewSet(viewsets.ModelViewSet):
    """API view for client order list"""
    queryset = models.ModelOrder.objects.all()
    serializer_class = serializers.ClientOrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.OrderFilter

    def get_queryset(self):
        return self.queryset.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        serializer = serializers.ClientOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_data = serializer.save()
        functions.create_order_in_firebase(saved_data)
        return Response(serializer.data)
