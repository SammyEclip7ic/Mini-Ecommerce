from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.orders.models import Order


class Payment(BaseModel):
    """
    Payment model to handle all payment transactions.
    One payment per order.
    """
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash on Delivery'),
        ('telebirr', 'Telebirr'),
        ('chapa', 'Chapa'),
        ('cbe', 'Commercial Bank of Ethiopia'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction details
    transaction_reference = models.CharField(max_length=255, unique=True)
    external_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Payment gateway response
    gateway_response = models.JSONField(null=True, blank=True)
    
    # Timestamps
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_reference']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_reference} - {self.status}"

    def mark_as_completed(self):
        from django.utils import timezone
        self.status = 'completed'
        self.paid_at = timezone.now()
        self.save()

    def mark_as_failed(self):
        self.status = 'failed'
        self.save()
