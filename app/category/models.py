import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

from django_fsm import FSMIntegerField
import requests
from core import imggenerate


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

    name = models.CharField(max_length=200, verbose_name="Название магазина")
    login = models.CharField(max_length=200, unique=True, verbose_name="Логин")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    avatar = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="Почта")
    address = models.CharField(max_length=200, null=True, verbose_name="Адресс")
    location = models.CharField(max_length=200, null=True, blank=True)
    slogan = models.CharField(max_length=200, null=True, blank=True, verbose_name="Слоган")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(default=5, verbose_name="Рейтинг")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Магазин")
        verbose_name_plural = ("Магазины")


class Category(models.Model):
    """Category model"""
    nameEn = models.CharField(max_length=200, null=True)
    nameRus = models.CharField(max_length=200, null=True)
    nameKg = models.CharField(max_length=200, null=True)
    icon = models.ImageField(null=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    store = models.ManyToManyField('User', blank=True)

    def __str__(self):
        return self.nameRus

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class SubCategory(models.Model):
    """SubCategory model"""
    nameEn = models.CharField(max_length=200, null=True)
    nameRus = models.CharField(max_length=200, null=True)
    nameKg = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Субкатегория")
        verbose_name_plural = ("Субгатегории")


class SubSubCategory(models.Model):
    """SubSubCategory model"""
    nameEn = models.CharField(max_length=200, null=True)
    nameRus = models.CharField(max_length=200, null=True)
    nameKg = models.CharField(max_length=200, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Субподкатегория")
        verbose_name_plural = ("Субподгатегории")