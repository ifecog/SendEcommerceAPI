# Generated by Django 5.0.7 on 2024-07-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_fragile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='medium', max_length=6),
        ),
    ]