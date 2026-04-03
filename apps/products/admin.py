from django.contrib import admin
from .models import Product, Category, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'vendor', 'category', 'price',
        'stock', 'is_active', 'average_rating', 'created_at'
    ]
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'vendor__shop_name']
    readonly_fields = [
        'slug', 'average_rating', 'total_reviews',
        'created_at', 'updated_at'
    ]
    inlines = [ProductImageInline]
    date_hierarchy = 'created_at'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['created_at', 'updated_at']
