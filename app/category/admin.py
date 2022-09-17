from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from category import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('login', 'phone', 'name')
    search_fields = ['login', ]
    list_filter = (
    )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'description', 'slogan', 'avatar', 'email', 'address', 'instagram', 'facebook', 'whatsapp', 'web', 'priority')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )


class RegularUserAdmin(admin.ModelAdmin):

    search_fields = ('name',)
    list_filter = (
        ('isoptovik', admin.BooleanFieldListFilter),
    )
    list_display = ['login', 'name', 'phone']

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'address', 'isoptovik',
                                         'optovik_start_date', 'optovik_end_date')}),
    )

# admin.site.register(models.User)
admin.site.register(models.Store, UserAdmin)
admin.site.register(models.RegularAccount, RegularUserAdmin)
admin.site.register(models.StoreCategory)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.SubSubCategory)