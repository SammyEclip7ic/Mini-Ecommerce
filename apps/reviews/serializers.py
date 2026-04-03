from rest_framework import serializers
from .models import Review, VendorRating


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'user_email',
            'product', 'product_name', 'rating', 'comment',
            'is_verified_purchase', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'is_verified_purchase',
            'created_at', 'updated_at'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs.get('product')
        
        # Check if user already reviewed this product
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product")
        
        # Check if user purchased this product
        from apps.orders.models import OrderItem
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            product=product,
            order__status__in=['paid', 'delivered']
        ).exists()
        
        if not has_purchased:
            raise serializers.ValidationError("You can only review products you have purchased")
        
        attrs['is_verified_purchase'] = True
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VendorRatingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.fullName', read_only=True)
    vendor_name = serializers.CharField(source='vendor.shop_name', read_only=True)
    
    class Meta:
        model = VendorRating
        fields = [
            'id', 'customer', 'customer_name',
            'vendor', 'vendor_name', 'stars', 'feedback',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'customer', 'created_at', 'updated_at']

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, attrs):
        customer = self.context['request'].user
        vendor = attrs.get('vendor')
        
        # Check if customer already rated this vendor
        if VendorRating.objects.filter(customer=customer, vendor=vendor).exists():
            raise serializers.ValidationError("You have already rated this vendor")
        
        # Check if customer has purchased from this vendor
        from apps.orders.models import OrderItem
        has_purchased = OrderItem.objects.filter(
            order__user=customer,
            vendor=vendor,
            order__status__in=['paid', 'delivered']
        ).exists()
        
        if not has_purchased:
            raise serializers.ValidationError("You can only rate vendors you have purchased from")
        
        return attrs

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
