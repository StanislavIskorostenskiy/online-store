# Generated by Django 4.2.1 on 2023-06-11 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0004_catalog_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='subcategories',
        ),
    ]