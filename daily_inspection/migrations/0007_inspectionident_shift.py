# Generated by Django 5.1.5 on 2025-01-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_inspection', '0006_dailyinspection_inspection_ident'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectionident',
            name='shift',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
