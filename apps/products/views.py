from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsVendor, IsOwnerOrReadOnly
from .filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [IsVendor()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user

        if not user.status:
            raise PermissionError("Blocked vendor")

        serializer.save(vendor=user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_products(self, request):
        products = Product.objects.filter(vendor=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
