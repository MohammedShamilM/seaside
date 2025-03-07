# Generated by Django 5.1.3 on 2025-01-09 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_order_items_product_alter_order_items_variant'),
        ('products', '0011_variant_is_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variant'),
        ),
    ]
