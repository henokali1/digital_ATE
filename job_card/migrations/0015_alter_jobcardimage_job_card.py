# Generated by Django 5.1.5 on 2025-03-22 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_card', '0014_remove_jobcardimage_message_jobcardimage_job_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcardimage',
            name='job_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='job_card.jobcard'),
        ),
    ]
