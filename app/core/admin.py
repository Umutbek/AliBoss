from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy


from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('login', 'phone')

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'description', 'avatar', 'email', 'address')}),

        (_('Important dates'), {'fields': ('last_login',)})

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )

class CartItemsAdmin(admin.StackedInline):
    model = models.CartItems


class ModelOrderAdmin(admin.ModelAdmin):
    inlines = [CartItemsAdmin]

    list_display = ('id', 'phone', 'address', 'date', 'status', 'totalCost')

    fieldsets = (
        (_('Информация о заказе'), {'fields': ('store', 'totalCost', 'user', 'address', 'phone',
                                         'comment', 'storeName', 'storeLogo', 'status')}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Item)
admin.site.register(models.ModelOrder, ModelOrderAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
