from django.contrib import admin
from .models import Review, VendorRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'product', 'rating',
        'is_verified_purchase', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['user__email', 'product__name', 'comment']
    readonly_fields = ['created_at', 'updated_at', 'is_verified_purchase']
    date_hierarchy = 'created_at'


@admin.register(VendorRating)
class VendorRatingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'vendor', 'stars', 'created_at']
    list_filter = ['stars', 'created_at']
    search_fields = ['customer__email', 'vendor__shop_name', 'feedback']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
