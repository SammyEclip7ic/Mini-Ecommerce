
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('vendors/', include('apps.vendors.urls'))
]
