from .models import Cart, CartItem
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        models = Cart
        fields = ['id', 'user', 'created_at', 'items']