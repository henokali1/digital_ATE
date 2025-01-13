from django.contrib import admin
from .models import JobCard

@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = ('job_card_number', 'task_description', 'status')
    list_filter = ('status', 'priority_level', 'location')
    search_fields = ('job_card_number', 'task_description')
