# Generated by Django 3.1 on 2022-03-10 19:58

import core.imggenerate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220310_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='currency',
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Фото'),
        ),
    ]
