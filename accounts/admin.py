# accounts/admin.py ---

from django.contrib import admin
from .models import UserProfile, Position
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_position') # Add get_position
    list_select_related = ('userprofile', 'userprofile__position') # Optimize query

    def get_position(self, instance):
        # Check if userprofile and position exist before accessing name
        if hasattr(instance, 'userprofile') and instance.userprofile.position:
             return instance.userprofile.position.name
        return None
    get_position.short_description = 'Position' # Column header

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Position model
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'can_create_job_cards') # Show the new flag in the list view
    list_editable = ('can_create_job_cards',) # Allow editing the flag directly in the list
    search_fields = ('name',)

# Optionally register UserProfile if needed separately (usually managed via User)
admin.site.register(UserProfile)
