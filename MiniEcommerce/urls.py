"""
URL configuration for MiniEcommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to CampusConnect Mini-Ecommerce API',
        'version': '1.0',
        'endpoints': {
            'accounts': '/api/v1/accounts/',
            'vendors': '/api/v1/vendors/',
            'products': '/api/v1/products/',
            'categories': '/api/v1/products/categories/',
            'cart': '/api/v1/cart/',
            'orders': '/api/v1/orders/',
            'payments': '/api/v1/payments/',
            'reviews': '/api/v1/reviews/',
            'wishlist': '/api/v1/wishlist/',
            'notifications': '/api/v1/notifications/',
            'admin': '/admin/',
        },
        'authentication': {
            'register': '/api/v1/accounts/auth/register/',
            'login': '/api/v1/accounts/auth/login/',
            'refresh': '/api/v1/accounts/auth/token/refresh/',
            'profile': '/api/v1/accounts/auth/profile/',
        },
        'documentation': 'See API_DOCUMENTATION.md for complete API reference'
    })


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'service': 'CampusConnect Mini-Ecommerce API'})


urlpatterns = [
    path('', api_root, name='api-root'),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/', api_root, name='api-v1-root'),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/vendors/', include('apps.vendors.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/cart/', include('apps.cart.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/wishlist/', include('apps.wishlist.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/chat/', include('apps.chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = "CampusConnect Mini-Ecommerce Administration"
admin.site.site_title = "CampusConnect Admin"
admin.site.index_title = "Welcome to CampusConnect Mini-Ecommerce Admin"
