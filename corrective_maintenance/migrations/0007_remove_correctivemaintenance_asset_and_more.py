# Generated by Django 5.1.5 on 2025-03-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0020_assethistory'),
        ('corrective_maintenance', '0006_correctivemaintenance_rosi_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correctivemaintenance',
            name='asset',
        ),
        migrations.AddField(
            model_name='correctivemaintenance',
            name='asset',
            field=models.ManyToManyField(related_name='corrective_maintenances', to='asset.asset'),
        ),
    ]
