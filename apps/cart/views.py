from apps.products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

class CartAddItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role == 'vendor':
            raise PermissionDenied("Vendors cannot add items to a cart.")

        cart, created = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, ValueError):
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity <= 0:
                return Response({"error": "Quantity must be positive"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid quantity format"}, status=status.HTTP_400_BAD_REQUEST)

        if quantity > product.stock:
            return Response({"error": f"Only {product.stock} items in stock"}, status=status.HTTP_400_BAD_REQUEST)

        existing_item = CartItem.objects.filter(cart=cart, product=product).first()

        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                return Response({"error": "Total quantity exceeds stock"}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_item.quantity = new_quantity
            existing_item.save()
            return Response({"message": "Cart updated", "item": CartItemSerializer(existing_item).data})

        item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)