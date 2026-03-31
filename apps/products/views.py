from rest_framework import viewsets, generics, status, filters, serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.accounts.permissions import IsVendor # From Person 1
from apps.vendors.models import Vendor
from django.db.models import QuerySet

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Task: Filtering (Category, Price Range)
    filterset_fields = {
        'category__name': ['icontains'],
        'price': ['gte', 'lte'],
    }
    # Task: Search
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsVendor()]
        return []

    def perform_create(self, serializer):
        # Task: Ensure user has a vendor profile and is approved
        vendor_profile = Vendor.objects.get(user=self.request.user)
        if not vendor_profile.isApproved:
            raise serializers.ValidationError("Your vendor account is not yet approved.")
        serializer.save(vendor=vendor_profile)

    
class VendorDashboardView(generics.ListAPIView):
    """
    Task: Vendor product dashboard
    Endpoint: GET /vendors/:id/products
    """
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]

    def get_queryset(self) -> QuerySet: # type: ignore
        vendor_id = self.kwargs.get('vendor_id')
        return Product.objects.filter(vendor__id=vendor_id)