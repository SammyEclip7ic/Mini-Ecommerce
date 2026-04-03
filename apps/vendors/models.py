from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Vendor(BaseModel):
    """
    Vendor profile model linked to User.
    Only users with role='vendor' can have a vendor profile.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='vendor_profile'
    )
    shop_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendors/logos/', null=True, blank=True)
    
    # Approval system
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Business metrics
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"{self.shop_name} - {self.user.email}"

    def approve(self):
        from django.utils import timezone
        self.is_approved = True
        self.approved_at = timezone.now()
        self.rejection_reason = ''
        self.save()

    def reject(self, reason: str):
        self.is_approved = False
        self.rejection_reason = reason
        self.save()