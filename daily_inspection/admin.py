
# daily_inspection/admin.py
from django.contrib import admin
from .models import DailyInspection

@admin.register(DailyInspection)
class DailyInspectionAdmin(admin.ModelAdmin):
    list_display = ['asset', 'shift', 'status', 'inspected_by', 'inspected_at', 'inspection_progress']
    list_filter = ['shift', 'status', 'inspected_at']
    search_fields = ['asset__name', 'inspected_by__username', 'remarks']
    readonly_fields = ['inspected_at', 'inspected_by', 'inspection_progress']
