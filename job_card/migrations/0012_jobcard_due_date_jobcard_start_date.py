# Generated by Django 5.1.4 on 2025-01-31 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_card', '0011_delete_scheduledjobcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobcard',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
