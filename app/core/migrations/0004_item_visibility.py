# Generated by Django 4.0.3 on 2022-12-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_servicecategory_servicesubcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='visibility',
            field=models.BooleanField(default=False, verbose_name='Видимость'),
        ),
    ]
