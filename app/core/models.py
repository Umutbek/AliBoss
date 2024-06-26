import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

from django_fsm import FSMIntegerField
import requests

from category.utils import SaleType
from core import imggenerate, utils, firestore
from category.models import Category, SubCategory, SubSubCategory, User, Store, RegularAccount


class Item(models.Model):
    """Model for Items"""
    name = models.CharField(max_length=500, verbose_name="Название товара")
    description = models.TextField(null=True, blank=True, verbose_name="Описание товара")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория товара")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сабкатегория товара")
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Субподкатегория товара")
    cost = models.FloatField(default=0, verbose_name="Цена товара")
    issale = models.BooleanField(default=False, verbose_name="Акционный товар?")
    costSale = models.FloatField(default=0, verbose_name="Акционная цена товара")
    supplier = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Магазин")
    uniqueid = models.CharField(max_length=200, null=True, blank=True, verbose_name="Штрихкод")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    imagelink = models.TextField(null=True, blank=True, verbose_name="Линк фото товара")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    instagram = models.CharField(max_length=200, null=True, blank=True, verbose_name="Инстаграм")
    facebook = models.CharField(max_length=200, null=True, blank=True, verbose_name="Фейсбук")
    whatsapp = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ватсап")
    web = models.CharField(max_length=200, null=True, blank=True, verbose_name="Веб")
    likes = models.IntegerField(default=0, verbose_name="Число лайков")
    views = models.IntegerField(default=0, verbose_name="Число просмотров")
    sale_type = FSMIntegerField(choices=SaleType.choices, default=SaleType.retail,
                                verbose_name='Тип продажи')
    isoptovik = models.BooleanField(default=False, verbose_name="Оптовый товар")
    optovikcost = models.FloatField(default=0, verbose_name="Оптовая цена товара")
    priority = models.FloatField(default=0, verbose_name="Приоритет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Список товаров")


class ModelOrder(models.Model):
    """Model for orders"""
    store = models.IntegerField(default=0, verbose_name="ID Магазина")
    totalCost = models.IntegerField(default=0, verbose_name="Общая сумма")
    user = models.CharField(max_length=200, null=True, blank=True, verbose_name="Пользователь")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Адресс")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарии")
    storeName = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название магазина")
    storeLogo = models.CharField(max_length=200, null=True, blank=True, verbose_name="Лого магазина")
    status = FSMIntegerField(choices=utils.OrderStatuses.choices, default=utils.OrderStatuses.New, verbose_name="Статус")
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    isoptovik = models.BooleanField(default=False, verbose_name="Оптовик?")
    bonus = models.FloatField(verbose_name='Бонус', default=0)
    pay_status = models.BooleanField(verbose_name='Статус оплаты', default=False)
    user_id = models.ForeignKey(to=RegularAccount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ID пользователя')

    @property
    def items(self):
        return self.cartitems_set.all()

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):

        try:
            firestore.db.collection(u'orders').document(
                str(self.id)).update({"status": self.status})
        except:
            pass

        super(ModelOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Заказ")
        verbose_name_plural = ("Заказы")


class CartItems(models.Model):
    """Models for images"""
    order = models.ForeignKey(ModelOrder, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="Товар")
    quantity = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")


class ServiceCategory(models.Model):
    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'

    category_title = models.CharField(max_length=100, verbose_name='Навание категории')

    def __str__(self):
        return self.category_title


class ServiceSubCategory(models.Model):
    class Meta:
        verbose_name = 'Подкатегория услуги'
        verbose_name_plural = 'Подкатегории услуг'

    sub_cat_title = models.CharField(max_length=100, verbose_name='Название подкатегории')
    categories = models.ForeignKey(to=ServiceCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.sub_cat_title


class Services(models.Model):
    """Model for services"""
    name = models.CharField(max_length=500, verbose_name="Название услуги")
    services_category = models.ForeignKey(to=ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    services_sub_category = models.ForeignKey(to=ServiceSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание услуги")
    cost = models.FloatField(default=0, verbose_name="Цена услуги")
    costSale = models.FloatField(default=0, verbose_name="Акционная цена услуги")
    issale = models.BooleanField(default=False)
    supplier = models.CharField(max_length=500, null=True, blank=True, verbose_name="Магазин")
    image = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    imagelink = models.TextField(null=True, blank=True, verbose_name="Линк фото товара")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    instagram = models.CharField(max_length=200, null=True, blank=True, verbose_name="Инстаграм")
    facebook = models.CharField(max_length=200, null=True, blank=True, verbose_name="Фейсбук")
    whatsapp = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ватсап")
    web = models.CharField(max_length=200, null=True, blank=True, verbose_name="Веб")
    likes = models.IntegerField(default=0, verbose_name="Число лайков")
    views = models.IntegerField(default=0, verbose_name="Число просмотров")
    priority = models.FloatField(default=0, verbose_name="Приоритет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Услуга")
        verbose_name_plural = ("Услуги")


class Banner(models.Model):
    """Model for banner advertisements"""
    photo = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото банерной рекламы")
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name="Линк")
    color = models.CharField(max_length=200, null=True, blank=True, verbose_name="Цвет")
    isoptovik = models.BooleanField(default=False, verbose_name="Оптовик?")

    class Meta:
        verbose_name = ("Банерная реклама")
        verbose_name_plural = ("Банерные рекламы")


class BonusHistory(models.Model):
    class Meta:
        verbose_name = ('История изменения бонуса')
        verbose_name_plural = ('История изменения бонусов')

    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    amount = models.FloatField(verbose_name='Сумма')
    user = models.ForeignKey(RegularAccount, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(to=ModelOrder, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.user.name)


class Notifications(models.Model):
    desc = models.CharField(verbose_name='Descriptions', max_length=100)
    title = models.CharField(max_length=100)
    itemId = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)
