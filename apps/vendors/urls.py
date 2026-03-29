from django.urls import path
from .views import CreateVendorView, VendorProfileView, UpdateVendorView

urlpatterns = [
    path('', CreateVendorView.as_view()),
    path('me/', VendorProfileView.as_view()),
    path('update/', UpdateVendorView.as_view()),
]