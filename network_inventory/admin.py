from django.contrib import admin
from .models import NetworkInventory

@admin.register(NetworkInventory)
class NetworkInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'section', 'manufacturer', 'mac_address')
    search_fields = ('name', 'ip', 'manufacturer')  # Add fields to search
    list_filter = ('section', 'manufacturer')  # Add filters to the sidebar
