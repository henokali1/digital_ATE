# Generated by Django 5.1.4 on 2025-01-12 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preventive_maintenance', '0005_rename_ppm_form_preventivemaintenance_ppm_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='preventivemaintenance',
            name='duration',
            field=models.FloatField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='preventivemaintenance',
            name='end_date',
            field=models.DateField(default='2025-01-01'),
        ),
        migrations.AddField(
            model_name='preventivemaintenance',
            name='end_time',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AddField(
            model_name='preventivemaintenance',
            name='start_date',
            field=models.DateField(default='2025-01-01'),
        ),
        migrations.AddField(
            model_name='preventivemaintenance',
            name='start_time',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
