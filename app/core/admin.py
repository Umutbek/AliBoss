from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Item)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.SubSubCategory)

