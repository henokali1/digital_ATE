# Generated by Django 5.1.4 on 2025-01-10 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preventive_maintenance', '0003_rename_form_uploads_preventivemaintenance_ppm_form'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preventivemaintenance',
            old_name='ppm_form',
            new_name='PPM_form',
        ),
    ]
