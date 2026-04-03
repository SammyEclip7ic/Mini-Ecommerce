from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import (
    PaymentSerializer,
    PaymentInitializeSerializer,
    PaymentVerifySerializer
)
from .services import PaymentService
from apps.orders.models import Order
from apps.notifications.services import NotificationService
from apps.core.pagination import StandardResultsSetPagination


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Return payments for the authenticated user only.
        """
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all().select_related('user', 'order')
        return Payment.objects.filter(user=user).select_related('order')

    @action(detail=False, methods=['post'])
    def initialize(self, request):
        """
        Initialize a payment for an order.
        """
        serializer = PaymentInitializeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']
        callback_url = serializer.validated_data.get(
            'callback_url',
            request.build_absolute_uri('/api/v1/payments/webhook/')
        )

        order = get_object_or_404(Order, id=order_id)

        try:
            # Create payment record
            payment = PaymentService.create_payment(order, payment_method)

            # Initialize payment with gateway
            result = PaymentService.initialize_payment(payment, callback_url)

            if result.get('success'):
                # Create notification
                NotificationService.notify_order_placed(request.user, order)

                response_data = {
                    'payment': PaymentSerializer(payment).data,
                    'checkout_url': result.get('checkout_url'),
                    'message': result.get('message')
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                payment.delete()
                return Response(
                    {'error': result.get('message')},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a payment status.
        """
        payment = self.get_object()

        result = PaymentService.verify_payment(payment)

        if result.get('success'):
            if result.get('status') == 'completed':
                NotificationService.notify_payment_success(
                    request.user, payment)

            return Response({
                'payment': PaymentSerializer(payment).data,
                'verification': result
            })
        else:
            NotificationService.notify_payment_failed(request.user, payment)
            return Response(
                {'error': result.get('message')},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentWebhookView(APIView):
    """
    Handle webhook callbacks from payment gateways.
    """
    permission_classes = []  # Webhooks don't use authentication

    def post(self, request, payment_method):
        """
        Handle webhook POST request.
        """
        result = PaymentService.handle_webhook(payment_method, request.data)

        if result.get('success'):
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
