# Generated by Django 5.0.3 on 2024-03-14 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]