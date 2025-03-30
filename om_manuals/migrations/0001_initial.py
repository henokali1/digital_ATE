# Generated by Django 5.1.5 on 2025-03-30 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=255)),
                ('section', models.CharField(blank=True, max_length=255, null=True)),
                ('folder', models.CharField(blank=True, max_length=255, null=True)),
                ('file_type', models.CharField(blank=True, max_length=50, null=True)),
                ('indexed_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
