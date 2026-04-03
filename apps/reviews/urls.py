from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, VendorRatingViewSet

router = DefaultRouter()
router.register(r'products', ReviewViewSet, basename='review')
router.register(r'vendors', VendorRatingViewSet, basename='vendor-rating')

urlpatterns = [
    path('', include(router.urls)),
]
