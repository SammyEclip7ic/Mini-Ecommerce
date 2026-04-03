from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.shop_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'vendor', 'vendor_name', 'product',
            'product_name', 'product_price', 'quantity',
            'subtotal', 'created_at'
        ]
        read_only_fields = [
            'id', 'product_name', 'product_price',
            'subtotal', 'created_at'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'total_price',
            'status', 'delivery_location', 'delivery_notes',
            'items', 'payment_status',
            'paid_at', 'shipped_at', 'delivered_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'total_price', 'status',
            'paid_at', 'shipped_at', 'delivered_at',
            'created_at', 'updated_at'
        ]

    def get_payment_status(self, obj):
        if hasattr(obj, 'payment'):
            return {
                'method': obj.payment.payment_method,
                'status': obj.payment.status,
                'transaction_reference': obj.payment.transaction_reference
            }
        return None


class CheckoutSerializer(serializers.Serializer):
    delivery_location = serializers.CharField(max_length=255)
    delivery_notes = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=['cash', 'telebirr', 'chapa', 'cbe']
    )

    def validate(self, attrs):
        # Validate that user has items in cart
        user = self.context['request'].user
        from apps.cart.models import Cart
        
        try:
            cart = Cart.objects.get(user=user)
            if not cart.items.exists():
                raise serializers.ValidationError("Cart is empty")
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found")
        
        return attrs
