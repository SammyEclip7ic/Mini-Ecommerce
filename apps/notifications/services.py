from .models import Notification
from typing import Optional
import uuid


class NotificationService:
    """
    Service layer for creating notifications.
    """
    
    @staticmethod
    def create_notification(
        user,
        notification_type: str,
        title: str,
        message: str,
        reference_id: Optional[uuid.UUID] = None,
        reference_type: Optional[str] = None
    ) -> Notification:
        """
        Create a new notification for a user.
        """
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            reference_id=reference_id,
            reference_type=reference_type
        )

    @staticmethod
    def notify_order_placed(user, order):
        """
        Notify user when order is placed.
        """
        return NotificationService.create_notification(
            user=user,
            notification_type='order_placed',
            title='Order Placed Successfully',
            message=f'Your order #{str(order.id)[:8]} has been placed successfully.',
            reference_id=order.id,
            reference_type='order'
        )

    @staticmethod
    def notify_payment_success(user, payment):
        """
        Notify user when payment is successful.
        """
        return NotificationService.create_notification(
            user=user,
            notification_type='payment_success',
            title='Payment Successful',
            message=f'Your payment of ETB {payment.amount} was successful.',
            reference_id=payment.id,
            reference_type='payment'
        )

    @staticmethod
    def notify_payment_failed(user, payment):
        """
        Notify user when payment fails.
        """
        return NotificationService.create_notification(
            user=user,
            notification_type='payment_failed',
            title='Payment Failed',
            message=f'Your payment of ETB {payment.amount} failed. Please try again.',
            reference_id=payment.id,
            reference_type='payment'
        )
