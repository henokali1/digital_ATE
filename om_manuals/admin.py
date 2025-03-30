from django.contrib import admin
from .models import Manual
from .utils import index_manuals, remove_deleted_manuals
from django.contrib import messages

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'folder', 'file_type')
    actions = ['reindex_manuals']

    @admin.action(description='Reindex Manuals')
    def reindex_manuals(self, request, queryset):
        index_manuals()
        remove_deleted_manuals()
        self.message_user(request, "Manuals reindexed successfully.", level=messages.SUCCESS)