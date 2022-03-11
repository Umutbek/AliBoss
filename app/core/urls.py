from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'item'

router = SimpleRouter()

router.register(r'item', views.ItemViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'subcategory', views.SubCategoryViewSet)
router.register(r'subsubcategory', views.SubSubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
