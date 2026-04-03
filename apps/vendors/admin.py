from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'shop_name', 'user', 'is_approved',
        'total_orders', 'total_sales', 'created_at'
    ]
    list_filter = ['is_approved', 'created_at']
    search_fields = ['shop_name', 'user__email', 'user__fullName']
    readonly_fields = ['created_at', 'updated_at', 'approved_at', 'total_sales', 'total_orders']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'shop_name', 'description', 'phone_number', 'address', 'logo')
        }),
        ('Approval Status', {
            'fields': ('is_approved', 'approved_at', 'rejection_reason')
        }),
        ('Business Metrics', {
            'fields': ('total_sales', 'total_orders')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
