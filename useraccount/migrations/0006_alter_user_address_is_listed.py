# Generated by Django 5.1.3 on 2024-12-24 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0005_user_address_is_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_address',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]
