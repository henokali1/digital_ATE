# Generated by Django 5.1.5 on 2025-02-22 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spare_parts', '0005_remove_sparepart_installation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sparepart',
            name='position_rack',
        ),
    ]
