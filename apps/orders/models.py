from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.products.models import Product
from apps.vendors.models import Vendor


class Order(BaseModel):
    """
    Order model representing a customer's order.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    delivery_location = models.CharField(max_length=255)
    delivery_notes = models.TextField(blank=True)
    
    # Timestamps for status changes
    paid_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order {str(self.id)[:8]} - {self.user.email}"

    def mark_as_paid(self):
        from django.utils import timezone
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()

    def mark_as_shipped(self):
        from django.utils import timezone
        self.status = 'shipped'
        self.shipped_at = timezone.now()
        self.save()

    def mark_as_delivered(self):
        from django.utils import timezone
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()


class OrderItem(BaseModel):
    """
    Individual items in an order.
    Snapshot of product at time of purchase.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    
    # Snapshot fields - preserve data even if product changes
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    # Calculated field
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def save(self, *args, **kwargs):
        # Calculate subtotal before saving
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)
