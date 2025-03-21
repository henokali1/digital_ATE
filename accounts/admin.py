from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Position

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_staff_id_no', 'get_position_name', 'ate_staff')

    def get_staff_id_no(self, obj):
        return obj.userprofile.staff_id_no
    get_staff_id_no.short_description = 'Staff ID'

    def get_position_name(self, obj):
        if obj.userprofile.position:
            return obj.userprofile.position.name
        return None  # Or return "No Position" or similar
    get_position_name.short_description = 'Position'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def ate_staff(self, obj):
        return obj.userprofile.ate_staff
    ate_staff.boolean = True #This will display a checkmark
    ate_staff.short_description = 'ATE Staff'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#Register Position model
admin.site.register(Position)
