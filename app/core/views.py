from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect

from category.models import RegularAccount
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
    search_fields = ('storeName', )

    def get_queryset(self):
        return self.queryset.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ClientOrderSerializerGet
        return serializers.ClientOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.ClientOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_data = serializer.save()
        if request.data['status'] == 4:
            user_id = serializer.data['user_id']
            if user_id is not None:
                user = models.RegularAccount.objects.get(pk=user_id)
                store = models.Store.objects.get(pk=saved_data.store)
                if store.cashback != 0 and store.cashback is not None:
                    bonus = float(saved_data.bonus)
                    if bonus != 0 and bonus is not None:
                        user.bonus -= bonus
                        user.save()
                        models.BonusHistory.objects.create(user_id=user_id, amount=bonus * -1, order_id=saved_data.id)

                    totalCost = float(request.data['totalCost'])
                    add_bonus = totalCost * (store.cashback / 100)
                    user.bonus += add_bonus
                    user.save()
                    models.BonusHistory.objects.create(user_id=request.data['user_id'], amount=add_bonus,
                                                       order_id=saved_data.id)

        functions.create_order_in_firebase(saved_data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = serializers.ClientOrderSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.data['status'] == 4:
            user_id = serializer.data['user_id']
            if user_id is not None:
                user = models.RegularAccount.objects.get(pk=user_id)
                store = models.Store.objects.get(pk=serializer.data['store'])
                if store.cashback != 0 and store.cashback is not None:
                    bonus = float(serializer.data['bonus'])
                    if bonus != 0 and bonus is not None:
                        user.bonus -= bonus
                        user.save()
                        models.BonusHistory.objects.create(user_id=user_id, amount=bonus * -1, order_id=serializer.data['id'])

                    totalCost = float(serializer.data['totalCost'])
                    add_bonus = totalCost * (store.cashback / 100)
                    user.bonus += add_bonus
                    user.save()
                    models.BonusHistory.objects.create(user_id=serializer.data['user_id'], amount=add_bonus,
                                                       order_id=serializer.data['id'])

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class BonusHistoryApi(viewsets.ModelViewSet):
    """API view for client order list"""
    queryset = models.BonusHistory.objects.all()
    serializer_class = serializers.BonusHistorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.BonusHistoryFilter


class AddBonusView(APIView):
    serializer_class = serializers.AddBonusSerializer

    def post(self, request):
        serializer = serializers.AddBonusSerializer(data=request.data)
        try:
            user = models.RegularAccount.objects.get(pk=request.data['user'])
            bonus = request.data['bonus']
            user.bonus += int(bonus)
            user.save()
            bonusHistory = models.BonusHistory.objects.create(amount=bonus, user=user)
            bonusHistory.save()
            return Response({'Success': 'OK!'}, status=209)
        except RegularAccount.DoesNotExist:
            raise Http404('ERROR! User with this ID was not found!')


class NotificationApi(APIView):
    serializer = serializers.NotificationSerializer

    def post(self, request):
        serializer = serializers.NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_data = serializer.save()
        functions.create_notification_in_fire_base(saved_data)
        return Response({"success": "ok"}, status=200)


