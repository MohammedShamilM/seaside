# Generated by Django 5.1.3 on 2024-12-17 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0003_rename_address_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_address',
            name='country',
        ),
    ]
