# Generated by Django 4.0.4 on 2022-05-13 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Furniture', '0004_rename_user_mycart_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycart',
            old_name='user_name',
            new_name='cart_user_name',
        ),
    ]
