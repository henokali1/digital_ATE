# Generated by Django 5.1.4 on 2025-01-15 02:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrective_maintenance', '0003_remove_correctivemaintenance_job_card_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='correctivemaintenance',
            name='completed_by',
            field=models.ManyToManyField(related_name='correctie_maintenance_completed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
