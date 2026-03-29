from django.db import models

import uuid
from django.db import models

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        'accounts.User',   # 🔗 connects to your User model
        on_delete=models.CASCADE,
        related_name='vendor'
    )

    shopName = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    isApproved = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shopName
