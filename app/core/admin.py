from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from core import models
from django.utils.html import format_html, mark_safe


class CartItemsAdmin(admin.StackedInline):
    model = models.CartItems


class ModelOrderAdmin(admin.ModelAdmin):
    inlines = [CartItemsAdmin]

    list_display = ('id', 'phone', 'address', 'date', 'status', 'totalCost')

    fieldsets = (
        (_('Информация о заказе'), {'fields': ('store', 'totalCost', 'user', 'address', 'phone',
                                         'comment', 'storeName', 'storeLogo', 'status')}),
    )


class ItemAdmin(admin.ModelAdmin):

    def image_tag(self, obj):

        try:
            if obj.imagelink:
                return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.imagelink))

            else:
                return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.image.url))

        except:
            pass

    image_tag.short_description = 'Фото товара'
    image_tag.allow_tags = True

    list_display = ('name', 'cost', 'image_tag')
    readonly_fields = ('image_tag',)

    search_fields = ('name',)
    list_filter = (
        ('isoptovik', admin.BooleanFieldListFilter),
    )


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Services)
admin.site.register(models.ServiceCategory)
admin.site.register(models.ServiceSubCategory)
admin.site.register(models.Banner)

admin.site.register(models.ModelOrder, ModelOrderAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
