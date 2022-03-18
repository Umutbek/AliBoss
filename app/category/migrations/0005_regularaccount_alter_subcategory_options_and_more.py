# Generated by Django 4.0.3 on 2022-03-18 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularAccount',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('uid', models.CharField(max_length=200, verbose_name='Код пользователя')),
                ('isoptovik', models.BooleanField(default=False)),
                ('optovik_start_date', models.DateTimeField(blank=True, null=True)),
                ('optovik_end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('category.user',),
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('id',), 'verbose_name': 'Субкатегория', 'verbose_name_plural': 'Субгатегории'},
        ),
        migrations.AlterModelOptions(
            name='subsubcategory',
            options={'ordering': ('id',), 'verbose_name': 'Субподкатегория', 'verbose_name_plural': 'Субподгатегории'},
        ),
        migrations.RemoveField(
            model_name='store',
            name='address',
        ),
        migrations.RemoveField(
            model_name='store',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=200, null=True, verbose_name='Адресс'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Телефон номер'),
        ),
    ]