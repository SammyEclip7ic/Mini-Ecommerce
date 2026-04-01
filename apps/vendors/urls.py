from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.views import ProductViewSet, CategorySerializer

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
