# Generated by Django 4.0.3 on 2023-01-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_item_sale_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonushistory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
