# Generated by Django 3.1 on 2022-03-10 19:48

import core.imggenerate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=200, unique=True, verbose_name='Логин'),
        ),
    ]
