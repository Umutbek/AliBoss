# Generated by Django 4.0.3 on 2022-05-13 04:54

import core.imggenerate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_item_priority_services_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Фото'),
        ),
    ]
