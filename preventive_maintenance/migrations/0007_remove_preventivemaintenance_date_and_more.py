# Generated by Django 5.1.4 on 2025-01-12 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preventive_maintenance', '0006_preventivemaintenance_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preventivemaintenance',
            name='date',
        ),
        migrations.RemoveField(
            model_name='preventivemaintenance',
            name='time',
        ),
    ]
