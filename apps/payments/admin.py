from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_reference', 'order', 'payment_method',
        'amount', 'status', 'created_at'
    ]
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['transaction_reference', 'order__id', 'user__email']
    readonly_fields = [
        'id', 'transaction_reference', 'created_at',
        'updated_at', 'paid_at'
    ]
    date_hierarchy = 'created_at'
