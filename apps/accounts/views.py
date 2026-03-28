from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer

class RegisterAPIView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows anyone to create a new user account.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return success message and user data (excluding password)
        return Response({
            "message": "User registered successfully.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(TokenObtainPairView):
    """
    API view for user login.
    Uses the custom LoginSerializer to authenticate with email.
    """
    serializer_class = LoginSerializer
