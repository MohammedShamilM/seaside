# Generated by Django 5.1.3 on 2025-01-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_order_items_product_alter_order_items_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
