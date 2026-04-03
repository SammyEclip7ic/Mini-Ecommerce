from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from apps.cart.models import Cart
from apps.payments.services import PaymentService
from apps.notifications.services import NotificationService
from apps.core.pagination import StandardResultsSetPagination


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing orders.
    
    list: Get all orders for the authenticated user
    retrieve: Get a specific order
    checkout: Create order from cart
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Order.objects.all().select_related('user').prefetch_related('items')
        elif user.role == 'vendor':
            # Vendors see orders containing their products
            from apps.vendors.models import Vendor
            try:
                vendor = Vendor.objects.get(user=user)
                return Order.objects.filter(
                    items__vendor=vendor
                ).distinct().select_related('user').prefetch_related('items')
            except Vendor.DoesNotExist:
                return Order.objects.none()
        else:
            # Customers see their own orders
            return Order.objects.filter(user=user).prefetch_related('items')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Create an order from the user's cart.
        """
        if request.user.role == 'vendor':
            raise PermissionDenied("Vendors cannot place orders")

        serializer = CheckoutSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        delivery_location = serializer.validated_data['delivery_location']
        delivery_notes = serializer.validated_data.get('delivery_notes', '')
        payment_method = serializer.validated_data['payment_method']
        
        # Get user's cart
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use transaction to ensure atomicity
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.total_price,
                    delivery_location=delivery_location,
                    delivery_notes=delivery_notes
                )
                
                # Create order items and reduce stock
                for cart_item in cart.items.select_related('product', 'product__vendor'):
                    product = cart_item.product
                    
                    # Verify stock availability
                    if product.stock < cart_item.quantity:
                        raise ValueError(f"Insufficient stock for {product.name}")
                    
                    # Create order item with snapshot
                    OrderItem.objects.create(
                        order=order,
                        vendor=product.vendor,
                        product=product,
                        product_name=product.name,
                        product_price=product.price,
                        quantity=cart_item.quantity
                    )
                    
                    # Reduce stock
                    product.stock -= cart_item.quantity
                    product.save()
                    
                    # Update vendor metrics
                    vendor = product.vendor
                    vendor.total_orders += 1
                    vendor.save()
                
                # Create payment
                payment = PaymentService.create_payment(order, payment_method)
                
                # Initialize payment with gateway
                callback_url = request.build_absolute_uri('/api/v1/payments/webhook/')
                payment_result = PaymentService.initialize_payment(payment, callback_url)
                
                if not payment_result.get('success'):
                    raise ValueError(payment_result.get('message', 'Payment initialization failed'))
                
                # Clear cart
                cart.items.all().delete()
                
                # Create notification
                NotificationService.notify_order_placed(request.user, order)
                
                # Prepare response
                response_data = {
                    'order': OrderSerializer(order).data,
                    'payment': {
                        'transaction_reference': payment.transaction_reference,
                        'payment_method': payment.payment_method,
                        'amount': str(payment.amount),
                        'status': payment.status,
                        'checkout_url': payment_result.get('checkout_url')
                    },
                    'message': 'Order placed successfully'
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order (only if pending).
        """
        order = self.get_object()
        
        # Only order owner can cancel
        if order.user != request.user and request.user.role != 'admin':
            raise PermissionDenied("You don't have permission to cancel this order")
        
        if order.status not in ['pending', 'paid']:
            return Response(
                {"error": "Only pending or paid orders can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restore stock
        with transaction.atomic():
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
            
            order.status = 'cancelled'
            order.save()
        
        return Response({
            "message": "Order cancelled successfully",
            "order": OrderSerializer(order).data
        })
