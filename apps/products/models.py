from django.db import models
from django.utils.text import slugify
from apps.core.models import BaseModel
from apps.vendors.models import Vendor


class Category(BaseModel):
    """
    Product category model.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(BaseModel):
    """
    Product model with vendor relationship.
    """
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=300, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Aggregated fields
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        help_text="Average rating from reviews"
    )
    total_reviews = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vendor', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            import uuid
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def update_rating(self):
        """
        Update average rating based on reviews.
        """
        from django.db.models import Avg, Count
        from apps.reviews.models import Review
        
        stats = Review.objects.filter(product=self).aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        
        self.average_rating = stats['avg_rating'] or 0
        self.total_reviews = stats['count'] or 0
        self.save()


class ProductImage(BaseModel):
    """
    Product image model for multiple images per product.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.product.name}"