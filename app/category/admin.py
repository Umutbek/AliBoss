from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _


from django.utils.html import format_html, mark_safe
from category import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('login', 'phone', 'name', 'visibility', 'image_tag')
    search_fields = ['login', ]
    list_filter = (
        'storecategory',
    )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'description', 'sale_type', 'slogan', 'avatar', 'email', 'address',
                                         'instagram', 'facebook', 'whatsapp', 'web', 'priority', 'cashback',
                                         'storecategory', 'visibility')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )

    def image_tag(self, obj):
        try:
            if obj.avatar:
                return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.avatar.url))

            else:
                return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.avatar.url))
        except:
            pass

    image_tag.short_description = 'Логотип'
    image_tag.allow_tags = True

    readonly_fields = ('image_tag',)


class RegularUserAdmin(admin.ModelAdmin):

    search_fields = ('name',)
    list_filter = (
        ('isoptovik', admin.BooleanFieldListFilter),
    )
    list_display = ['login', 'name', 'phone']

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'address', 'isoptovik', 'bonus', 'magazin',
                                         'optovik_start_date', 'optovik_end_date')}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'nameRus']
    list_display_links = ['id', 'nameRus']
    ordering = ['-priority', ]


# admin.site.register(models.User)
admin.site.register(models.Store, UserAdmin)
admin.site.register(models.RegularAccount, RegularUserAdmin)
admin.site.register(models.StoreCategory)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.SubCategory)
admin.site.register(models.SubSubCategory)
