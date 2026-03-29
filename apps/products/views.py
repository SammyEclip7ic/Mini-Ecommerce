from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

from products.pagination import CustomPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-createdAt')

        # SEARCH
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        # FILTERING
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)

        min_price = self.request.query_params.get('minPrice')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.query_params.get('maxPrice')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
    

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'vendor':
            raise PermissionDenied("Only vendors can create products")

        vendor = user.vendor

        if not vendor.isApproved:
            raise PermissionDenied("Vendor not approved")

        serializer.save(vendor=vendor)
    
    
    def perform_update(self, serializer):
        product = self.get_object()

        if product.vendor != self.request.user.vendor:
            raise PermissionDenied("Not your product")

        serializer.save()


    def perform_destroy(self, instance):
        if instance.vendor != self.request.user.vendor:
            raise PermissionDenied("Not your product")

        instance.delete()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VendorProductDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'vendor':
            raise PermissionDenied("Only vendors allowed")

        vendor = request.user.vendor

        products = Product.objects.filter(vendor=vendor)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)