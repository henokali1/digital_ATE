# Generated by Django 5.1.4 on 2025-01-07 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_alter_asset_manufacturer_alter_asset_model_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='manufacturer',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='asset',
            name='model_number',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='asset',
            name='part_number',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
