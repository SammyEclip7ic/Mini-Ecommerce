from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.products.models import Product


class Cart(BaseModel):
    """
    Shopping cart model - one per user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def total_price(self):
        """
        Calculate total price of all items in cart.
        """
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """
        Get total number of items in cart.
        """
        return self.items.count()

    @property
    def total_quantity(self):
        """
        Get total quantity of all items.
        """
        return sum(item.quantity for item in self.items.all())


class CartItem(BaseModel):
    """
    Individual items in a cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        """
        Calculate subtotal for this cart item.
        """
        return self.product.price * self.quantity

    def clean(self):
        """
        Validate cart item before saving.
        """
        from django.core.exceptions import ValidationError
        
        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive")
        
        if self.quantity > self.product.stock:
            raise ValidationError(f"Only {self.product.stock} items available in stock")
