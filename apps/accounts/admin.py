from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'username', 'fullName', 'role',
        'status', 'is_staff', 'date_joined'
    ]
    list_filter = ['role', 'status', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'username', 'fullName']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('fullName', 'first_name', 'last_name')
        }),
        ('Role & Status', {
            'fields': ('role', 'status')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'fullName', 'role', 'password1', 'password2'),
        }),
    )
