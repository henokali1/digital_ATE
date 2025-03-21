# Generated by Django 5.1.4 on 2025-01-13 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrective_maintenance', '0002_correctivemaintenance_job_card_id'),
        ('job_card', '0004_remove_jobcard_corrective_maintenance_id_and_more'),
        ('preventive_maintenance', '0009_preventivemaintenance_job_card_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='corrective_maintenance_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corrective_maintenance.correctivemaintenance'),
        ),
        migrations.AddField(
            model_name='jobcard',
            name='preventive_maintenance_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='preventive_maintenance.preventivemaintenance'),
        ),
    ]
