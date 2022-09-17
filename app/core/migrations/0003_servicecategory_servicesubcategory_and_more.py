# Generated by Django 4.0.3 on 2022-09-17 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_servicesubcategory_categories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=100, verbose_name='Навание категории')),
            ],
            options={
                'verbose_name': 'Категория услуги',
                'verbose_name_plural': 'Категории услуг',
            },
        ),
        migrations.CreateModel(
            name='ServiceSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_cat_title', models.CharField(max_length=100, verbose_name='Название подкатегории')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.servicecategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория услуги',
                'verbose_name_plural': 'Подкатегории услуг',
            },
        ),
        migrations.AddField(
            model_name='services',
            name='services_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.servicecategory'),
        ),
        migrations.AddField(
            model_name='services',
            name='services_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.servicesubcategory'),
        ),
    ]
