# Generated by Django 4.0.4 on 2022-05-12 07:27

import Furniture.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Furniture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('interest', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(choices=[('S', 'Select'), ('M', 'Mumbai'), ('K', 'Kolkata'), ('B', 'Bengaluru'), ('G', 'Gujarat')], default='Select', max_length=20, validators=[Furniture.models.validate_city])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContactProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('phone_number', models.IntegerField()),
                ('user_email', models.EmailField(max_length=200)),
                ('user_message', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('furniture_image', models.ImageField(upload_to='images')),
                ('price', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Furniture.category')),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('selling_item', models.CharField(max_length=70)),
                ('fulfilled_by', models.CharField(max_length=20)),
                ('city', models.CharField(choices=[('S', 'Select'), ('M', 'Mumbai'), ('K', 'Kolkata'), ('B', 'Bengaluru'), ('G', 'Gujarat')], default='Select', max_length=20, validators=[Furniture.models.validate_city_seller])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriberProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('user_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
