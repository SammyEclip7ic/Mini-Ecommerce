from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Product, Category
from .serializers import CategorySerializer

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "limit": self.page_size,
            "total": self.page.paginator.count
        })
    
