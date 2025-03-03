# Generated by Django 5.1.5 on 2025-02-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='actual_behavior',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bugreport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bugreport',
            name='expected_behavior',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bugreport',
            name='steps_to_reproduce',
            field=models.TextField(blank=True, null=True),
        ),
    ]
