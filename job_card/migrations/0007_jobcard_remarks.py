# Generated by Django 5.1.5 on 2025-01-25 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_card', '0006_jobcard_acknowledged_jobcard_acknowledged_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
