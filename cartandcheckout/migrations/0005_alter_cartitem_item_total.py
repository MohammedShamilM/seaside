# Generated by Django 5.1.3 on 2025-02-21 14:57

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartandcheckout', '0004_rename_price_cartitem_item_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item_total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
