from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'subtotal', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_price', 'status',
        'delivery_location', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__email', 'delivery_location']
    readonly_fields = [
        'id', 'total_price', 'paid_at', 'shipped_at',
        'delivered_at', 'created_at', 'updated_at'
    ]
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'product_name', 'vendor',
        'quantity', 'product_price', 'subtotal'
    ]
    list_filter = ['vendor', 'created_at']
    search_fields = ['order__id', 'product_name', 'vendor__shop_name']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']
