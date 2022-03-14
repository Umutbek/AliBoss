from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'core'

router = SimpleRouter()

router.register(r'item', views.ItemViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'banner', views.BannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("order/", views.OrderView.as_view())
]
