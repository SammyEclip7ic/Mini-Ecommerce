from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['shopName', 'user', 'isApproved']
    list_filter = ['isApproved']