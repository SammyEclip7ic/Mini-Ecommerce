from rest_framework import serializers
from .models import Product, Category, ProductImage
from apps.vendors.models import Vendor

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'category', 'category_name', 'stock', 'images', 'uploaded_images'
        ]
        lookup_field = 'slug'

    def create(self, validated_data):
        images_data = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        return product