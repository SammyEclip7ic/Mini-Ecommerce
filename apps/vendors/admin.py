from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    # This controls which columns show up in the list view
    list_display = ('shopName', 'user', 'isApproved', 'createdAt')
    
    # This adds a sidebar filter for easy approval management
    list_filter = ('isApproved', 'createdAt')
    
    # This allows you to search for vendors by name or email
    search_fields = ('shopName', 'user__email')
    
    # This makes 'isApproved' editable directly from the list!
    list_editable = ('isApproved',)