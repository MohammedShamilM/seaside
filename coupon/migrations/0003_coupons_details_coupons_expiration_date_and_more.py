# Generated by Django 5.1.3 on 2025-01-10 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_alter_coupons_code_alter_coupons_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='details',
            field=models.CharField(default='dede', max_length=300),
        ),
        migrations.AddField(
            model_name='coupons',
            name='expiration_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
