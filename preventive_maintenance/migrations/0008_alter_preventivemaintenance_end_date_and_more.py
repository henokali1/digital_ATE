# Generated by Django 5.1.4 on 2025-01-12 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preventive_maintenance', '0007_remove_preventivemaintenance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
