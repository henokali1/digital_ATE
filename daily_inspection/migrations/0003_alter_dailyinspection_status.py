# Generated by Django 5.1.4 on 2025-01-21 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_inspection', '0002_alter_dailyinspection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyinspection',
            name='status',
            field=models.CharField(blank=True, choices=[('OK', 'Ok'), ('WARNING', 'Warning'), ('ALARM', 'Alarm'), ('DONE', 'Done'), ('OFF', 'Off'), ('UNSERVICEABLE', 'Unserviceable')], max_length=30, null=True),
        ),
    ]
