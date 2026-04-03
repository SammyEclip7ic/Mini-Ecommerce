from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_price', 'total_items']
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.total_items
    
    def total_price(self, obj):
        return obj.total_price


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__email', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'subtotal']

    def subtotal(self, obj):
        return obj.subtotal
