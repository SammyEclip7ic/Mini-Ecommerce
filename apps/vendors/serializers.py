from rest_framework import serializers
from .models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()


class VendorSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'user', 'user_email', 'user_name',
            'shop_name', 'description', 'phone_number',
            'address', 'logo', 'is_approved', 'approved_at',
            'rejection_reason', 'total_sales', 'total_orders',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'is_approved', 'approved_at',
            'total_sales', 'total_orders', 'created_at', 'updated_at'
        ]


class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['shop_name', 'description', 'phone_number', 'address', 'logo']

    def validate(self, attrs):
        user = self.context['request'].user
        
        # Check if user role is vendor
        if user.role != 'vendor':
            raise serializers.ValidationError("Only users with vendor role can create a vendor profile")
        
        # Check if vendor profile already exists
        if Vendor.objects.filter(user=user).exists():
            raise serializers.ValidationError("Vendor profile already exists for this user")
        
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VendorDashboardSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_orders = serializers.IntegerField()
    recent_orders = serializers.ListField()
