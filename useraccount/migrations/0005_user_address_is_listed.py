# Generated by Django 5.1.3 on 2024-12-24 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_remove_user_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='is_listed',
            field=models.BooleanField(default=False),
        ),
    ]
