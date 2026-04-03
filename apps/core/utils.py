import hashlib
import hmac
from decimal import Decimal
from typing import Dict, Any


def generate_transaction_reference(order_id: str, payment_method: str) -> str:
    """
    Generate a unique transaction reference for payment.
    """
    import time
    timestamp = str(int(time.time()))
    return f"{payment_method.upper()}-{order_id[:8]}-{timestamp}"


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """
    Verify webhook signature for payment callbacks.
    """
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)


def calculate_percentage(amount: Decimal, percentage: float) -> Decimal:
    """
    Calculate percentage of an amount.
    """
    return amount * Decimal(str(percentage / 100))


def format_currency(amount: Decimal, currency: str = 'ETB') -> str:
    """
    Format amount as currency string.
    """
    return f"{currency} {amount:,.2f}"
