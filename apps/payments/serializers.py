from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source='order.id', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'user_email', 'payment_method',
            'amount', 'status', 'transaction_reference',
            'external_transaction_id', 'paid_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'transaction_reference', 'external_transaction_id',
            'status', 'paid_at', 'created_at', 'updated_at'
        ]


class PaymentInitializeSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    payment_method = serializers.ChoiceField(
        choices=['cash', 'telebirr', 'chapa', 'cbe']
    )
    callback_url = serializers.URLField(required=False)

    def validate_order_id(self, value):
        from apps.orders.models import Order
        try:
            order = Order.objects.get(id=value)
            
            # Check if order belongs to the user
            if order.user != self.context['request'].user:
                raise serializers.ValidationError("You don't have permission to pay for this order")
            
            # Check if payment already exists
            if hasattr(order, 'payment'):
                raise serializers.ValidationError("Payment already exists for this order")
            
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")


class PaymentVerifySerializer(serializers.Serializer):
    transaction_reference = serializers.CharField()
