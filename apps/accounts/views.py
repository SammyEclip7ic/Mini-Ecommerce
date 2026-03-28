from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

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

class ProfileAPIView(generics.RetrieveAPIView):
    """
    API view for user profile.
    Retrieve the profile of the currently logged-in user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the current authenticated user.
        """
        return self.request.user
