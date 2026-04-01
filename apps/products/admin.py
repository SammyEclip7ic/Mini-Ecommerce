from django.contrib import admin
from .models import Product, Category, ProductImage

# Register Category simply
admin.site.register(Category)

# Optional: This allows you to see/add images directly inside the Product page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'stock', 'slug')
    list_filter = ('category', 'vendor', 'createdAt')
    search_fields = ('name', 'description')
    
    # This tells Django the slug is read-only in the admin
    readonly_fields = ('slug',)
    
    # Adds the image upload rows to the bottom of the product page
    inlines = [ProductImageInline]
