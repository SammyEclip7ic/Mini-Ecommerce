from rest_framework import serializers
from .models import Wishlist
from apps.products.serializers import ProductSerializer


class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_details', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_product(self, value):
        """
        Check that the product is not already in the user's wishlist.
        """
        user = self.context['request'].user
        if Wishlist.objects.filter(user=user, product=value).exists():
            raise serializers.ValidationError("This product is already in your wishlist.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WishlistCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value
