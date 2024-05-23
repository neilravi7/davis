# Generated by Django 4.2.4 on 2024-05-23 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=250)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditems', to='menu.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'food_item',
            },
        ),
    ]
