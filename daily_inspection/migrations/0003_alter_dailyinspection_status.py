# Generated by Django 5.1.4 on 2025-01-19 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_inspection', '0002_dailyinspection_inspected_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyinspection',
            name='status',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
