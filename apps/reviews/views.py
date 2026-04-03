from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg
from .models import Review, VendorRating
from .serializers import ReviewSerializer, VendorRatingSerializer
from apps.core.pagination import StandardResultsSetPagination
from apps.core.permissions import IsOwner


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product reviews.
    
    list: Get all reviews (filtered by product if specified)
    retrieve: Get a specific review
    create: Create a review (verified buyers only)
    update: Update own review
    destroy: Delete own review
    """
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsOwner()]

    def get_queryset(self):
        queryset = Review.objects.all().select_related('user', 'product')
        
        # Filter by product if specified
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        
        # Filter by user if specified
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """
        Get all reviews by the authenticated user.
        """
        reviews = Review.objects.filter(user=request.user).select_related('product')
        
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='product/(?P<product_id>[^/.]+)/stats')
    def product_stats(self, request, product_id=None):
        """
        Get review statistics for a product.
        """
        reviews = Review.objects.filter(product__id=product_id)
        
        stats = {
            'total_reviews': reviews.count(),
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'rating_distribution': {
                '5': reviews.filter(rating=5).count(),
                '4': reviews.filter(rating=4).count(),
                '3': reviews.filter(rating=3).count(),
                '2': reviews.filter(rating=2).count(),
                '1': reviews.filter(rating=1).count(),
            }
        }
        
        return Response(stats)


class VendorRatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vendor ratings.
    
    list: Get all vendor ratings (filtered by vendor if specified)
    retrieve: Get a specific rating
    create: Create a vendor rating (verified customers only)
    update: Update own rating
    destroy: Delete own rating
    """
    serializer_class = VendorRatingSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsOwner()]

    def get_queryset(self):
        queryset = VendorRating.objects.all().select_related('customer', 'vendor')
        
        # Filter by vendor if specified
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        
        return queryset

    @action(detail=False, methods=['get'], url_path='vendor/(?P<vendor_id>[^/.]+)/stats')
    def vendor_stats(self, request, vendor_id=None):
        """
        Get rating statistics for a vendor.
        """
        ratings = VendorRating.objects.filter(vendor__id=vendor_id)
        
        stats = {
            'total_ratings': ratings.count(),
            'average_rating': ratings.aggregate(Avg('stars'))['stars__avg'] or 0,
            'rating_distribution': {
                '5': ratings.filter(stars=5).count(),
                '4': ratings.filter(stars=4).count(),
                '3': ratings.filter(stars=3).count(),
                '2': ratings.filter(stars=2).count(),
                '1': ratings.filter(stars=1).count(),
            }
        }
        
        return Response(stats)
