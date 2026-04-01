from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from apps.cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # 1. Get the user's cart
        try:
            cart = Cart.objects.get(user=user)
            if not cart.items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Use a transaction to ensure either everything works or nothing changes
        with transaction.atomic():
            # Create the main Order
            order = Order.objects.create(
                user=user,
                total_price=cart.total_price,
                delivery_location=request.data.get('delivery_location', 'Default Location'),
                payment_method=request.data.get('payment_method', 'cash')
            )

            # 3. Create OrderItems and reduce stock
            for cart_item in cart.items.all():
                product = cart_item.product
                
                # Double-check stock one last time
                if product.stock < cart_item.quantity:
                    raise Exception(f"Not enough stock for {product.name}")

                # Create the snapshot item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    vendor=product.vendor, # Link to the vendor dashboard
                    quantity=cart_item.quantity,
                    price=product.price # Save current price
                )

                # Reduce stock in the products app
                product.stock -= cart_item.quantity
                product.save()

            # 4. Clear the cart after successful order
            cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)