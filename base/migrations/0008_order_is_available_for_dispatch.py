# Generated by Django 5.0.7 on 2024-08-06 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_available_for_dispatch',
            field=models.BooleanField(default=False),
        ),
    ]