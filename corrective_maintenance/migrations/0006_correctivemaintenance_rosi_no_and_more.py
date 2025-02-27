# Generated by Django 5.1.4 on 2025-01-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrective_maintenance', '0005_alter_correctivemaintenance_preventive_action_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='correctivemaintenance',
            name='ROSI_NO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='correctivemaintenance',
            name='incident_report',
            field=models.FileField(blank=True, null=True, upload_to='uploads/incident_reports/'),
        ),
    ]
