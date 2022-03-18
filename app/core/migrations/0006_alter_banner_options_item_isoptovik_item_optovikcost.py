# Generated by Django 4.0.3 on 2022-03-18 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_banner_services_alter_modelorder_lat_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': 'Банерная реклама', 'verbose_name_plural': 'Банерные рекламы'},
        ),
        migrations.AddField(
            model_name='item',
            name='isoptovik',
            field=models.BooleanField(default=False, verbose_name='Оптовый товар'),
        ),
        migrations.AddField(
            model_name='item',
            name='optovikcost',
            field=models.FloatField(default=0, verbose_name='Оптовая цена товара'),
        ),
    ]