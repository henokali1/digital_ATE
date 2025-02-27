# Generated by Django 5.1.4 on 2025-01-18 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_positionrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='position_rack',
            field=models.ForeignKey(blank=True, help_text='Position or rack where the asset is located', null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.positionrack'),
        ),
    ]
