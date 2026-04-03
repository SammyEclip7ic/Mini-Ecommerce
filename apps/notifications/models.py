from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Notification(BaseModel):
    """
    Notification model for event-driven notifications.
    """
    NOTIFICATION_TYPES = (
        ('order_placed', 'Order Placed'),
        ('order_accepted', 'Order Accepted'),
        ('order_rejected', 'Order Rejected'),
        ('order_delivered', 'Order Delivered'),
        ('payment_success', 'Payment Success'),
        ('payment_failed', 'Payment Failed'),
        ('product_low_stock', 'Product Low Stock'),
        ('vendor_approved', 'Vendor Approved'),
        ('vendor_rejected', 'Vendor Rejected'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Optional reference to related objects
    reference_id = models.UUIDField(null=True, blank=True)
    reference_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.title}"

    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
