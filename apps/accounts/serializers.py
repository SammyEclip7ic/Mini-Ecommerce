from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'fullName', 'password', 'role')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'fullName': {'required': True},
            'role': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            fullName=validated_data['fullName'],
            password=validated_data['password'],
            role=validated_data.get('role', 'customer')
        )
        return user

class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT login.
    Uses 'email' as the username field for authentication.
    """
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom data to the response if needed
        # For example, user details
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'fullName': self.user.fullName,
            'role': self.user.role,
        }
        
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to return basic user information.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'fullName', 'role')
