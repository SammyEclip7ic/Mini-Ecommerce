from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VendorProductDashboard

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('vendor/dashboard/', VendorProductDashboard.as_view()),
]