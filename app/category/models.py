import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

from django_fsm import FSMIntegerField
import requests
from core import imggenerate, firestore


class StoreCategory(models.Model):
    """Model for store categories(types of stores(electronics, etc))"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")
    icon = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Категория магазина")
        verbose_name_plural = ("Категории магазинов")


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, login, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not login:
            raise ValueError('User must have an Email or Phone')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        """create a superuser"""
        user = self.create_user(login, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for user"""
    name = models.CharField(max_length=200, verbose_name="Название")
    login = models.CharField(max_length=200, unique=True, verbose_name="Логин")
    address = models.CharField(max_length=200, null=True, verbose_name="Адресс")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    avatar = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'


class RegularAccount(User):
    """Model for regular account"""
    uid = models.CharField(max_length=200, unique=True, verbose_name="Код пользователя")
    isoptovik = models.BooleanField(default=False, verbose_name="Оптовик?")
    optovik_start_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала работы оптовика")
    optovik_end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания оптовика")
    magazin = models.CharField(verbose_name='Магазин', max_length=100, null=True, blank=True)
    bonus = models.FloatField(verbose_name='Бонус', default=0)

    def save(self, *args, **kwargs):
        try:
            firestore.db.collection(u'users').document(self.uid).update(
                {"optovik": self.isoptovik})
        except:
            pass

        super(RegularAccount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")


class Store(User):
    """Model for user"""
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="Почта")
    location = models.CharField(max_length=200, null=True, blank=True)
    slogan = models.CharField(max_length=200, null=True, blank=True, verbose_name="Слоган")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    instagram = models.CharField(max_length=200, null=True, blank=True, verbose_name="Инстаграм")
    facebook = models.CharField(max_length=200, null=True, blank=True, verbose_name="Фейсбук")
    whatsapp = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ватсап")
    web = models.CharField(max_length=200, null=True, blank=True, verbose_name="Веб")
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    storecategory = models.ManyToManyField('StoreCategory', verbose_name="Категория магазина")
    priority = models.FloatField(default=0, verbose_name="Приоритет")
    rating = models.FloatField(default=5, verbose_name="Рейтинг")
    visibility = models.BooleanField(verbose_name="Видимость", default=True)
    cashback = models.FloatField(verbose_name='Кэш бэк', default=0)

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Магазин")
        verbose_name_plural = ("Магазины")


class Category(models.Model):
    """Category model"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")
    isoptovik = models.BooleanField(default=False, verbose_name="Оптовик?")
    priority = models.FloatField(default=0, verbose_name="Приоритет")

    icon = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    store = models.ManyToManyField('Store', blank=True, verbose_name="Магазин")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class SubCategory(models.Model):
    """SubCategory model"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="Категория")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Субкатегория")
        verbose_name_plural = ("Субгатегории")


class SubSubCategory(models.Model):
    """SubSubCategory model"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name="Подкатегория")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Субподкатегория")
        verbose_name_plural = ("Субподгатегории")
