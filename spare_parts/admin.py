from django.contrib import admin
from .models import SparePart, SparePartPhoto, CalibrationHistory, MaintenanceHistory, MaintenancePhoto

class SparePartPhotoInline(admin.TabularInline):
    model = SparePartPhoto
    extra = 1

class CalibrationHistoryInline(admin.TabularInline):
    model = CalibrationHistory
    extra = 1

class MaintenanceHistoryInline(admin.TabularInline):
    model = MaintenanceHistory
    extra = 1

class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'part_number', 'location', 'section', 'status')
    list_filter = ('location', 'section', 'status', 'manufacturer')
    search_fields = ('name', 'serial_number', 'part_number', 'description')
    inlines = [SparePartPhotoInline, CalibrationHistoryInline, MaintenanceHistoryInline]
    fieldsets = (
        (None, {
            'fields': (
                'name', 'serial_number', 'part_number', 'description', 'tag_id',
                'section', 'location', 'quantity', 'status', 'manufacturer', 'model_number'
            )
        }),
        ('Storage Details', {
            'fields': ('shelf_number', 'shelf_level', 'box_number', 'min_stock_level', 'pr_number'),
            'classes': ('collapse',)  # Optional: Collapse this section by default
        }),
    )

class MaintenancePhotoAdmin(admin.ModelAdmin):
    list_display = ('maintenance_history', 'photo')

admin.site.register(SparePart, SparePartAdmin)
admin.site.register(SparePartPhoto)
admin.site.register(CalibrationHistory)
admin.site.register(MaintenanceHistory)
admin.site.register(MaintenancePhoto, MaintenancePhotoAdmin)
