# Generated by Django 5.0.3 on 2024-03-26 12:25

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh', editable=False, length=10, max_length=30, prefix='vend', unique=True),
        ),
    ]