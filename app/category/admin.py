from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from category import models


class UserAdmin(BaseUserAdmin):

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.filter(is_superuser=False)
        return qs

    ordering = ['id']
    list_display = ('login', 'phone')

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'description', 'slogan', 'avatar', 'email', 'address', 'instagram', 'facebook', 'whatsapp', 'web')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )

# admin.site.register(models.User)
admin.site.register(models.Store, UserAdmin)

admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.SubSubCategory)