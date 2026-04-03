from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product, Category
from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    CategorySerializer
)
from apps.accounts.permissions import IsVendor
from apps.vendors.models import Vendor
from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsVendorOwner


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    
    list: Get all active categories (public)
    retrieve: Get a specific category (public)
    create: Create category (admin only)
    update: Update category (admin only)
    destroy: Delete category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    
    list: Get all active products (public)
    retrieve: Get a specific product (public)
    create: Create product (vendor only)
    update: Update product (vendor owner only)
    destroy: Delete product (vendor owner only)
    """
    queryset = Product.objects.filter(is_active=True).select_related(
        'vendor', 'category'
    ).prefetch_related('images')
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    
    # Filtering
    filterset_fields = {
        'category__name': ['icontains'],
        'category__slug': ['exact'],
        'price': ['gte', 'lte'],
        'stock': ['gte'],
    }
    
    # Search
    search_fields = ['name', 'description', 'vendor__shop_name']
    
    # Ordering
    ordering_fields = ['price', 'created_at', 'average_rating', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsVendor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsVendorOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by vendor if specified
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        
        # Show all products (including inactive) for vendor owners
        if self.request.user.is_authenticated and self.request.user.role == 'vendor':
            try:
                vendor = Vendor.objects.get(user=self.request.user)
                queryset = Product.objects.filter(vendor=vendor).select_related(
                    'vendor', 'category'
                ).prefetch_related('images')
            except Vendor.DoesNotExist:
                pass
        
        return queryset

    def perform_create(self, serializer):
        """
        Ensure user has an approved vendor profile.
        """
        try:
            vendor_profile = Vendor.objects.get(user=self.request.user)
            if not vendor_profile.is_approved:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Your vendor account is not yet approved.")
            serializer.save(vendor=vendor_profile)
        except Vendor.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must have a vendor profile to create products.")

    @action(detail=False, methods=['get'], permission_classes=[IsVendor])
    def my_products(self, request):
        """
        Get all products for the authenticated vendor.
        """
        try:
            vendor = Vendor.objects.get(user=request.user)
            products = Product.objects.filter(vendor=vendor).select_related(
                'category'
            ).prefetch_related('images')
            
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[IsVendorOwner])
    def toggle_active(self, request, slug=None):
        """
        Toggle product active status.
        """
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        
        return Response({
            "message": f"Product {'activated' if product.is_active else 'deactivated'}",
            "is_active": product.is_active
        })