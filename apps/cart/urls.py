from django.urls import path
from apps.cart.views import CartAddItem

urlpatterns = [
    path('add/', CartAddItem.as_view(), name='cart-add'),
]