from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistCreateSerializer
from apps.products.models import Product
from apps.core.pagination import StandardResultsSetPagination


class WishlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user wishlist.
    
    list: Get all wishlist items for the authenticated user
    create: Add a product to wishlist
    destroy: Remove a product from wishlist
    """
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Return wishlist items for the authenticated user only.
        """
        return Wishlist.objects.filter(user=self.request.user).select_related('product', 'product__vendor', 'product__category')

    def create(self, request, *args, **kwargs):
        """
        Add a product to the user's wishlist.
        """
        serializer = WishlistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_id = serializer.validated_data['product_id']
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return Response(
                {"error": "Product already in wishlist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist_item = Wishlist.objects.create(user=request.user, product=product)
        response_serializer = WishlistSerializer(wishlist_item)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='remove/(?P<product_id>[^/.]+)')
    def remove_by_product(self, request, product_id=None):
        """
        Remove a product from wishlist by product ID.
        """
        wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
        wishlist_item.delete()
        return Response(
            {"message": "Product removed from wishlist"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        Clear all items from the user's wishlist.
        """
        deleted_count = Wishlist.objects.filter(user=request.user).delete()[0]
        return Response(
            {"message": f"Removed {deleted_count} items from wishlist"},
            status=status.HTTP_204_NO_CONTENT
        )
