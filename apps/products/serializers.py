from rest_framework import serializers
from .models import Product, Category, ProductImage
from apps.vendors.models import Vendor


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'alt_text', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description',
            'image', 'is_active', 'products_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product lists.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.shop_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'stock',
            'category_name', 'vendor_name', 'primary_image',
            'average_rating', 'total_reviews', 'is_active'
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    """
    Detailed product serializer.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.shop_name', read_only=True)
    vendor_id = serializers.UUIDField(source='vendor.id', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'category', 'category_name', 'stock', 'is_active',
            'vendor_id', 'vendor_name', 'images', 'uploaded_images',
            'average_rating', 'total_reviews',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'vendor_id', 'average_rating',
            'total_reviews', 'created_at', 'updated_at'
        ]
        lookup_field = 'slug'

    def create(self, validated_data):
        images_data = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        
        for idx, image in enumerate(images_data):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(idx == 0)  # First image is primary
            )
        
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('uploaded_images', [])
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Add new images if provided
        if images_data:
            for image in images_data:
                ProductImage.objects.create(product=instance, image=image)
        
        return instance