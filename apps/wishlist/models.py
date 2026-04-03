from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.products.models import Product


class Wishlist(BaseModel):
    """
    User wishlist model.
    Each user can have multiple wishlist items.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
