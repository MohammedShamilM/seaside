# Generated by Django 5.1.3 on 2025-01-10 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]
