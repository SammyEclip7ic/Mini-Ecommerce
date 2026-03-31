import uuid
from django.db import models
from django.conf import settings

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='vendor_profile'
    )
    shopName = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    isApproved = models.BooleanField(default=False) # Important for Admin moderation
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shopName