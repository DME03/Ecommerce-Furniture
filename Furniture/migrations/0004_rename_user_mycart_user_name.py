# Generated by Django 4.0.4 on 2022-05-13 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Furniture', '0003_alter_furnitureitem_category_mycart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycart',
            old_name='user',
            new_name='user_name',
        ),
    ]