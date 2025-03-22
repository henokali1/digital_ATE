# Generated by Django 5.1.5 on 2025-03-22 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_inspection', '0003_alter_dailyinspection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyinspection',
            name='status',
            field=models.CharField(blank=True, choices=[('OK', 'Ok'), ('WARNING', 'Warning'), ('ALARM', 'Alarm'), ('DEGRADED', 'Degraded'), ('DONE', 'Done'), ('OFF', 'Off'), ('UNSERVICEABLE', 'Unserviceable')], max_length=30, null=True),
        ),
    ]
