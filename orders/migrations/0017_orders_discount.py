# Generated by Django 5.1.3 on 2025-01-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_orders_razorpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='discount',
            field=models.IntegerField(null=True),
        ),
    ]
