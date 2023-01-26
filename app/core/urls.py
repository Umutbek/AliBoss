from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'core'

router = SimpleRouter()

router.register(r'item', views.ItemViewSet)
router.register(r'services_category', views.ServiceCategoryViewSet)
router.register(r'services_sub_category', views.ServiceSubCategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'banner', views.BannerViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'bonusHistory', views.BonusHistoryApi)

urlpatterns = [
    path('', include(router.urls)),
    path('add_bonus/', views.AddBonusView.as_view()),
    path('notification/', views.NotificationApi.as_view()),
]
