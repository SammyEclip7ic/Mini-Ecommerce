from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)
from apps.products.models import Product


class CartViewSet(viewsets.ViewSet):
    """
    ViewSet for managing shopping cart.
    
    retrieve: Get current user's cart
    add_item: Add item to cart
    update_item: Update item quantity
    remove_item: Remove item from cart
    clear: Clear all items from cart
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Get the authenticated user's cart.
        """
        # Prevent vendors from accessing cart
        if request.user.role == 'vendor':
            raise PermissionDenied("Vendors cannot access shopping cart")
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Add an item to the cart or update quantity if already exists.
        """
        if request.user.role == 'vendor':
            raise PermissionDenied("Vendors cannot add items to cart")

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check stock availability
        if quantity > product.stock:
            return Response(
                {"error": f"Only {product.stock} items available in stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if item already in cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            # Update existing item
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return Response(
                    {"error": f"Total quantity would exceed stock. Only {product.stock} available"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
            message = "Cart item updated"
        else:
            message = "Item added to cart"
        
        return Response({
            "message": message,
            "cart_item": CartItemSerializer(cart_item, context={'request': request}).data
        }, status=status.HTTP_200_OK if not item_created else status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], url_path='update-item/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """
        Update the quantity of a cart item.
        """
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Check stock availability
        if quantity > cart_item.product.stock:
            return Response(
                {"error": f"Only {cart_item.product.stock} items available in stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            "message": "Cart item updated",
            "cart_item": CartItemSerializer(cart_item, context={'request': request}).data
        })

    @action(detail=False, methods=['delete'], url_path='remove-item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """
        Remove an item from the cart.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        Clear all items from the cart.
        """
        cart = get_object_or_404(Cart, user=request.user)
        deleted_count = cart.items.count()
        cart.items.all().delete()
        
        return Response(
            {"message": f"Removed {deleted_count} items from cart"},
            status=status.HTTP_204_NO_CONTENT
        )
