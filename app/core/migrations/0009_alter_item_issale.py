# Generated by Django 4.0.3 on 2022-03-22 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_modelorder_isoptovik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='issale',
            field=models.BooleanField(default=False, verbose_name='Акционный товар?'),
        ),
    ]