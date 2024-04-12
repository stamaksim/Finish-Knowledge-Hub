# Generated by Django 5.0.4 on 2024-04-12 16:35

from django.db import migrations
from knowhub.models import Category
import json


def create_categories_fixture(apps, schema_editor):
    with open('categories_fixture.json', 'r') as file:
        categories_data = json.load(file)

    for category_data in categories_data:
        Category.objects.create(**category_data)


class Migration(migrations.Migration):
    dependencies = [
        ('knowhub', '0012_alter_category_slug'),
    ]

    operations = [
        migrations.RunPython(create_categories_fixture),
    ]