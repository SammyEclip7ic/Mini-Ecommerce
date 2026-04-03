from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from .models import Vendor
from .serializers import (
    VendorSerializer,
    VendorCreateSerializer,
    VendorDashboardSerializer
)
from apps.accounts.permissions import IsVendor, IsAdmin
from apps.core.pagination import StandardResultsSetPagination
from apps.orders.models import OrderItem
from apps.orders.serializers import OrderSerializer


class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vendor profiles.
    
    list: Get all approved vendors (public)
    retrieve: Get a specific vendor (public)
    create: Create vendor profile (vendor role only)
    update: Update vendor profile (owner only)
    destroy: Delete vendor profile (owner only)
    """
    queryset = Vendor.objects.filter(is_approved=True)
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return VendorCreateSerializer
        return VendorSerializer

    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Vendor.objects.all()
        elif user.role == 'vendor':
            # Vendors can see their own profile even if not approved
            return Vendor.objects.filter(Q(is_approved=True) | Q(user=user))
        else:
            # Customers can only see approved vendors
            return Vendor.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Get the vendor profile of the authenticated user.
        """
        try:
            vendor = Vendor.objects.get(user=request.user)
            serializer = self.get_serializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], permission_classes=[IsVendor])
    def dashboard(self, request):
        """
        Get vendor dashboard statistics.
        """
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            return Response(
                {"error": "Vendor profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get statistics
        total_products = vendor.products.count()
        
        order_items = OrderItem.objects.filter(vendor=vendor)
        total_orders = order_items.values('order').distinct().count()
        
        total_revenue = order_items.filter(
            order__status__in=['paid', 'delivered']
        ).aggregate(
            total=Sum('price')
        )['total'] or 0
        
        pending_orders = order_items.filter(
            order__status='pending'
        ).values('order').distinct().count()
        
        # Get recent orders
        recent_order_items = order_items.select_related('order').order_by('-created_at')[:5]
        recent_orders = [
            {
                'order_id': str(item.order.id),
                'product': item.product.name if item.product else 'Deleted Product',
                'quantity': item.quantity,
                'price': str(item.price),
                'status': item.order.status,
                'created_at': item.created_at
            }
            for item in recent_order_items
        ]

        data = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'recent_orders': recent_orders
        }

        serializer = VendorDashboardSerializer(data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        """
        Approve a vendor (admin only).
        """
        vendor = self.get_object()
        vendor.approve()
        
        # Create notification
        from apps.notifications.services import NotificationService
        NotificationService.create_notification(
            user=vendor.user,
            notification_type='vendor_approved',
            title='Vendor Account Approved',
            message=f'Your vendor account "{vendor.shop_name}" has been approved!'
        )
        
        return Response({
            "message": "Vendor approved successfully",
            "vendor": VendorSerializer(vendor).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        """
        Reject a vendor (admin only).
        """
        vendor = self.get_object()
        reason = request.data.get('reason', 'No reason provided')
        vendor.reject(reason)
        
        # Create notification
        from apps.notifications.services import NotificationService
        NotificationService.create_notification(
            user=vendor.user,
            notification_type='vendor_rejected',
            title='Vendor Account Rejected',
            message=f'Your vendor account was rejected. Reason: {reason}'
        )
        
        return Response({
            "message": "Vendor rejected",
            "vendor": VendorSerializer(vendor).data
        })
