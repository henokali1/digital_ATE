# Generated by Django 5.1.4 on 2025-01-13 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corrective_maintenance', '0002_correctivemaintenance_job_card_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correctivemaintenance',
            name='job_card_id',
        ),
    ]
