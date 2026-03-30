from rest_framework.views import APIView
from .serializer import CartItemSerializer, CartSerializer
from .models import Cart, CartItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart , created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartAddItem(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = 