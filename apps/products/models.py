import uuid
from django.db import models
from django.utils.text import slugify

from apps.vendors.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    stock = models.IntegerField()

    slug = models.SlugField(unique=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')