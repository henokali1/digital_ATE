# Generated by Django 5.1.4 on 2025-01-10 10:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset', '0010_asset_remarks'),
        ('location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectiveMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('duration', models.FloatField(editable=False)),
                ('type', models.CharField(choices=[('General Problem', 'General Problem'), ('Outage', 'Outage'), ('Warning', 'Warning'), ('Alarm', 'Alarm')], max_length=50)),
                ('section', models.CharField(choices=[('Communication', 'Communication'), ('Navigation', 'Navigation'), ('Surveillance', 'Surveillance'), ('Aviation Networks', 'Aviation Networks'), ('Miscellaneous', 'Miscellaneous')], max_length=50)),
                ('corrective_action', models.TextField()),
                ('preventive_action', models.TextField()),
                ('root_cause', models.TextField()),
                ('remarks', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/corrective_photos/')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.asset')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
                ('logged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
