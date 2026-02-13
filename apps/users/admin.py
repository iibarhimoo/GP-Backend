from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission

# 1. Register the Permission Table
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_name', 'description')

# 2. Register the Role Table
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)
    filter_horizontal = ('permissions',) # Makes a nice selector for permissions

# 3. Register the Custom User Table (with Role support)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # This controls what you see in the list of users
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    
    # This controls the "Edit User" form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name')}),
        ('Role & Permissions', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    # Since we use email as username, we must set this
    ordering = ('email',)