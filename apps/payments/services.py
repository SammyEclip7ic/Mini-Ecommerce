from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from decimal import Decimal
import requests
from django.conf import settings
from .models import Payment
from apps.core.utils import generate_transaction_reference


class PaymentGateway(ABC):
    """
    Abstract base class for payment gateways.
    All payment providers must implement these methods.
    """
    
    @abstractmethod
    def initialize_payment(self, payment: Payment, callback_url: str) -> Dict[str, Any]:
        """
        Initialize payment with the gateway.
        Returns: dict with 'success', 'checkout_url', 'transaction_id', 'message'
        """
        pass

    @abstractmethod
    def verify_payment(self, transaction_reference: str) -> Dict[str, Any]:
        """
        Verify payment status with the gateway.
        Returns: dict with 'success', 'status', 'amount', 'message'
        """
        pass


class TelebirrService(PaymentGateway):
    """
    Telebirr payment gateway integration.
    """
    
    def __init__(self):
        self.api_url = getattr(settings, 'TELEBIRR_API_URL', 'https://api.telebirr.com')
        self.merchant_id = getattr(settings, 'TELEBIRR_MERCHANT_ID', '')
        self.api_key = getattr(settings, 'TELEBIRR_API_KEY', '')

    def initialize_payment(self, payment: Payment, callback_url: str) -> Dict[str, Any]:
        """
        Initialize Telebirr payment.
        """
        try:
            payload = {
                'merchant_id': self.merchant_id,
                'amount': str(payment.amount),
                'currency': 'ETB',
                'reference': payment.transaction_reference,
                'callback_url': callback_url,
                'customer_email': payment.user.email,
                'customer_name': payment.user.fullName,
            }
            
            # In production, make actual API call
            # response = requests.post(
            #     f"{self.api_url}/payment/initialize",
            #     json=payload,
            #     headers={'Authorization': f'Bearer {self.api_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'checkout_url': f'https://telebirr.com/checkout/{payment.transaction_reference}',
                'transaction_id': f'TBR-{payment.transaction_reference}',
                'message': 'Payment initialized successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to initialize payment: {str(e)}'
            }

    def verify_payment(self, transaction_reference: str) -> Dict[str, Any]:
        """
        Verify Telebirr payment status.
        """
        try:
            # In production, make actual API call
            # response = requests.get(
            #     f"{self.api_url}/payment/verify/{transaction_reference}",
            #     headers={'Authorization': f'Bearer {self.api_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'status': 'completed',
                'amount': '0.00',
                'message': 'Payment verified successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to verify payment: {str(e)}'
            }



class ChapaService(PaymentGateway):
    """
    Chapa payment gateway integration.
    """
    
    def __init__(self):
        self.api_url = getattr(settings, 'CHAPA_API_URL', 'https://api.chapa.co/v1')
        self.secret_key = getattr(settings, 'CHAPA_SECRET_KEY', '')

    def initialize_payment(self, payment: Payment, callback_url: str) -> Dict[str, Any]:
        """
        Initialize Chapa payment.
        """
        try:
            payload = {
                'amount': str(payment.amount),
                'currency': 'ETB',
                'tx_ref': payment.transaction_reference,
                'callback_url': callback_url,
                'return_url': callback_url,
                'email': payment.user.email,
                'first_name': payment.user.fullName.split()[0] if payment.user.fullName else 'Customer',
                'last_name': payment.user.fullName.split()[-1] if payment.user.fullName else 'User',
            }
            
            # In production, make actual API call
            # response = requests.post(
            #     f"{self.api_url}/transaction/initialize",
            #     json=payload,
            #     headers={'Authorization': f'Bearer {self.secret_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'checkout_url': f'https://checkout.chapa.co/{payment.transaction_reference}',
                'transaction_id': f'CHP-{payment.transaction_reference}',
                'message': 'Payment initialized successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to initialize payment: {str(e)}'
            }

    def verify_payment(self, transaction_reference: str) -> Dict[str, Any]:
        """
        Verify Chapa payment status.
        """
        try:
            # In production, make actual API call
            # response = requests.get(
            #     f"{self.api_url}/transaction/verify/{transaction_reference}",
            #     headers={'Authorization': f'Bearer {self.secret_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'status': 'completed',
                'amount': '0.00',
                'message': 'Payment verified successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to verify payment: {str(e)}'
            }


class CBEService(PaymentGateway):
    """
    Commercial Bank of Ethiopia payment gateway integration.
    """
    
    def __init__(self):
        self.api_url = getattr(settings, 'CBE_API_URL', 'https://api.cbe.com.et')
        self.merchant_code = getattr(settings, 'CBE_MERCHANT_CODE', '')
        self.api_key = getattr(settings, 'CBE_API_KEY', '')

    def initialize_payment(self, payment: Payment, callback_url: str) -> Dict[str, Any]:
        """
        Initialize CBE payment.
        """
        try:
            payload = {
                'merchant_code': self.merchant_code,
                'amount': str(payment.amount),
                'currency': 'ETB',
                'reference': payment.transaction_reference,
                'callback_url': callback_url,
                'customer_email': payment.user.email,
            }
            
            # In production, make actual API call
            # response = requests.post(
            #     f"{self.api_url}/payment/initialize",
            #     json=payload,
            #     headers={'Authorization': f'Bearer {self.api_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'checkout_url': f'https://payment.cbe.com.et/{payment.transaction_reference}',
                'transaction_id': f'CBE-{payment.transaction_reference}',
                'message': 'Payment initialized successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to initialize payment: {str(e)}'
            }

    def verify_payment(self, transaction_reference: str) -> Dict[str, Any]:
        """
        Verify CBE payment status.
        """
        try:
            # In production, make actual API call
            # response = requests.get(
            #     f"{self.api_url}/payment/verify/{transaction_reference}",
            #     headers={'Authorization': f'Bearer {self.api_key}'}
            # )
            
            # Simulated response for development
            return {
                'success': True,
                'status': 'completed',
                'amount': '0.00',
                'message': 'Payment verified successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to verify payment: {str(e)}'
            }


class PaymentService:
    """
    Main payment service that orchestrates payment operations.
    """
    
    @staticmethod
    def get_gateway(payment_method: str) -> Optional[PaymentGateway]:
        """
        Get the appropriate payment gateway based on payment method.
        """
        gateways = {
            'telebirr': TelebirrService,
            'chapa': ChapaService,
            'cbe': CBEService,
        }
        
        gateway_class = gateways.get(payment_method)
        return gateway_class() if gateway_class else None

    @staticmethod
    def create_payment(order, payment_method: str) -> Payment:
        """
        Create a payment record for an order.
        """
        # Check if payment already exists
        if hasattr(order, 'payment'):
            raise ValueError("Payment already exists for this order")

        transaction_ref = generate_transaction_reference(str(order.id), payment_method)
        
        payment = Payment.objects.create(
            user=order.user,
            order=order,
            payment_method=payment_method,
            amount=order.total_price,
            transaction_reference=transaction_ref,
            status='pending'
        )
        
        return payment

    @staticmethod
    def initialize_payment(payment: Payment, callback_url: str) -> Dict[str, Any]:
        """
        Initialize payment with the appropriate gateway.
        """
        if payment.payment_method == 'cash':
            # Cash on delivery doesn't need gateway initialization
            return {
                'success': True,
                'message': 'Cash on delivery selected',
                'payment_method': 'cash'
            }
        
        gateway = PaymentService.get_gateway(payment.payment_method)
        if not gateway:
            return {
                'success': False,
                'message': f'Unsupported payment method: {payment.payment_method}'
            }
        
        result = gateway.initialize_payment(payment, callback_url)
        
        if result.get('success'):
            payment.status = 'processing'
            payment.external_transaction_id = result.get('transaction_id')
            payment.gateway_response = result
            payment.save()
        
        return result

    @staticmethod
    def verify_payment(payment: Payment) -> Dict[str, Any]:
        """
        Verify payment status with the gateway.
        """
        if payment.payment_method == 'cash':
            return {
                'success': True,
                'status': 'pending',
                'message': 'Cash on delivery'
            }
        
        gateway = PaymentService.get_gateway(payment.payment_method)
        if not gateway:
            return {
                'success': False,
                'message': f'Unsupported payment method: {payment.payment_method}'
            }
        
        result = gateway.verify_payment(payment.transaction_reference)
        
        if result.get('success') and result.get('status') == 'completed':
            payment.mark_as_completed()
            
            # Update order status
            payment.order.status = 'paid'
            payment.order.save()
        
        return result

    @staticmethod
    def handle_webhook(payment_method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook callbacks from payment gateways.
        """
        try:
            transaction_ref = payload.get('transaction_reference') or payload.get('tx_ref')
            
            if not transaction_ref:
                return {'success': False, 'message': 'Missing transaction reference'}
            
            payment = Payment.objects.get(transaction_reference=transaction_ref)
            
            # Verify the payment
            result = PaymentService.verify_payment(payment)
            
            return result
            
        except Payment.DoesNotExist:
            return {'success': False, 'message': 'Payment not found'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
