from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel
from apps.products.models import Product
from apps.vendors.models import Vendor


class Review(BaseModel):
    """
    Product review model.
    Only verified buyers can review.
    One review per product per user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating}⭐"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update product rating after saving review
        self.product.update_rating()


class VendorRating(BaseModel):
    """
    Vendor rating model.
    Customers can rate vendors based on their experience.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_ratings_given'
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    feedback = models.TextField()

    class Meta:
        unique_together = ('customer', 'vendor')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.shop_name} - {self.stars}⭐"
