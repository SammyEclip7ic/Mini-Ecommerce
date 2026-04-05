# CampusConnect Mini-Ecommerce API Documentation

**Base URL:** `https://your-app-name.onrender.com`  
**API Version:** v1  
**Authentication:** JWT Bearer Token

---

## Quick Start

### 1. Authentication Flow

#### Register User
```javascript
POST /api/v1/accounts/auth/register/

// Request
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+251912345678"
}

// Response (201 Created)
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+251912345678"
}
```

#### Login
```javascript
POST /api/v1/accounts/auth/login/

// Request
{
  "username": "john_doe",
  "password": "securePassword123"
}

// Response (200 OK)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```javascript
POST /api/v1/accounts/auth/token/refresh/

// Request
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

// Response (200 OK)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get User Profile
```javascript
GET /api/v1/accounts/auth/profile/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+251912345678",
  "user_type": "customer",
  "is_verified": true
}
```

---

## 2. Products

#### List Products
```javascript
GET /api/v1/products/
GET /api/v1/products/?search=laptop
GET /api/v1/products/?category=1
GET /api/v1/products/?min_price=100&max_price=500
GET /api/v1/products/?ordering=-created_at

// Response (200 OK)
{
  "count": 50,
  "next": "http://api.example.com/api/v1/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "MacBook Pro",
      "description": "High-performance laptop",
      "price": "1299.99",
      "stock": 10,
      "category": {
        "id": 1,
        "name": "Electronics"
      },
      "vendor": {
        "id": 1,
        "business_name": "Tech Store"
      },
      "images": [
        {
          "id": 1,
          "image": "http://api.example.com/media/products/macbook.jpg",
          "is_primary": true
        }
      ],
      "average_rating": 4.5,
      "review_count": 23,
      "created_at": "2026-04-01T10:00:00Z"
    }
  ]
}
```

#### Get Product Detail
```javascript
GET /api/v1/products/{id}/

// Response (200 OK)
{
  "id": 1,
  "name": "MacBook Pro",
  "description": "High-performance laptop for professionals",
  "price": "1299.99",
  "stock": 10,
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics"
  },
  "vendor": {
    "id": 1,
    "business_name": "Tech Store",
    "rating": 4.8
  },
  "images": [...],
  "average_rating": 4.5,
  "review_count": 23,
  "specifications": {...},
  "created_at": "2026-04-01T10:00:00Z"
}
```

#### List Categories
```javascript
GET /api/v1/products/categories/

// Response (200 OK)
[
  {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics",
    "description": "Electronic devices and accessories",
    "product_count": 150
  }
]
```

---

## 3. Cart

#### Get Cart
```javascript
GET /api/v1/cart/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "MacBook Pro",
        "price": "1299.99",
        "image": "http://api.example.com/media/products/macbook.jpg"
      },
      "quantity": 2,
      "subtotal": "2599.98"
    }
  ],
  "total": "2599.98",
  "item_count": 2
}
```

#### Add to Cart
```javascript
POST /api/v1/cart/items/
Authorization: Bearer <access_token>

// Request
{
  "product_id": 1,
  "quantity": 2
}

// Response (201 Created)
{
  "id": 1,
  "product": {...},
  "quantity": 2,
  "subtotal": "2599.98"
}
```

#### Update Cart Item
```javascript
PATCH /api/v1/cart/items/{id}/
Authorization: Bearer <access_token>

// Request
{
  "quantity": 3
}

// Response (200 OK)
{
  "id": 1,
  "product": {...},
  "quantity": 3,
  "subtotal": "3899.97"
}
```

#### Remove from Cart
```javascript
DELETE /api/v1/cart/items/{id}/
Authorization: Bearer <access_token>

// Response (204 No Content)
```

#### Clear Cart
```javascript
DELETE /api/v1/cart/clear/
Authorization: Bearer <access_token>

// Response (204 No Content)
```

---

## 4. Orders

#### Create Order
```javascript
POST /api/v1/orders/
Authorization: Bearer <access_token>

// Request
{
  "shipping_address": {
    "street": "Bole Road",
    "city": "Addis Ababa",
    "state": "Addis Ababa",
    "postal_code": "1000",
    "country": "Ethiopia"
  },
  "payment_method": "telebirr"
}

// Response (201 Created)
{
  "id": 1,
  "order_number": "ORD-20260405-001",
  "status": "pending",
  "items": [...],
  "total": "2599.98",
  "shipping_address": {...},
  "payment_method": "telebirr",
  "created_at": "2026-04-05T10:00:00Z"
}
```

#### List Orders
```javascript
GET /api/v1/orders/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "order_number": "ORD-20260405-001",
      "status": "delivered",
      "total": "2599.98",
      "created_at": "2026-04-05T10:00:00Z"
    }
  ]
}
```

#### Get Order Detail
```javascript
GET /api/v1/orders/{id}/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "id": 1,
  "order_number": "ORD-20260405-001",
  "status": "delivered",
  "items": [
    {
      "product": {...},
      "quantity": 2,
      "price": "1299.99",
      "subtotal": "2599.98"
    }
  ],
  "total": "2599.98",
  "shipping_address": {...},
  "payment_status": "paid",
  "tracking_number": "TRK123456",
  "created_at": "2026-04-05T10:00:00Z"
}
```

---

## 5. Reviews

#### List Product Reviews
```javascript
GET /api/v1/reviews/?product={product_id}

// Response (200 OK)
{
  "count": 23,
  "results": [
    {
      "id": 1,
      "user": {
        "username": "john_doe",
        "first_name": "John"
      },
      "rating": 5,
      "comment": "Excellent product!",
      "created_at": "2026-04-01T10:00:00Z"
    }
  ]
}
```

#### Create Review
```javascript
POST /api/v1/reviews/
Authorization: Bearer <access_token>

// Request
{
  "product": 1,
  "rating": 5,
  "comment": "Excellent product! Highly recommended."
}

// Response (201 Created)
{
  "id": 1,
  "product": 1,
  "user": {...},
  "rating": 5,
  "comment": "Excellent product! Highly recommended.",
  "created_at": "2026-04-05T10:00:00Z"
}
```

---

## 6. Wishlist

#### Get Wishlist
```javascript
GET /api/v1/wishlist/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "MacBook Pro",
        "price": "1299.99",
        "image": "..."
      },
      "added_at": "2026-04-01T10:00:00Z"
    }
  ]
}
```

#### Add to Wishlist
```javascript
POST /api/v1/wishlist/items/
Authorization: Bearer <access_token>

// Request
{
  "product_id": 1
}

// Response (201 Created)
```

#### Remove from Wishlist
```javascript
DELETE /api/v1/wishlist/items/{id}/
Authorization: Bearer <access_token>

// Response (204 No Content)
```

---

## 7. Notifications

#### List Notifications
```javascript
GET /api/v1/notifications/
Authorization: Bearer <access_token>

// Response (200 OK)
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Order Shipped",
      "message": "Your order #ORD-20260405-001 has been shipped",
      "type": "order",
      "is_read": false,
      "created_at": "2026-04-05T10:00:00Z"
    }
  ]
}
```

#### Mark as Read
```javascript
PATCH /api/v1/notifications/{id}/
Authorization: Bearer <access_token>

// Request
{
  "is_read": true
}

// Response (200 OK)
```

---

## React Integration Example

### Setup Axios Instance

```javascript
// src/api/axios.js
import axios from 'axios';

const API_BASE_URL = 'https://your-app-name.onrender.com/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(
          `${API_BASE_URL}/accounts/auth/token/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

### Authentication Service

```javascript
// src/services/authService.js
import api from '../api/axios';

export const authService = {
  async register(userData) {
    const response = await api.post('/accounts/auth/register/', userData);
    return response.data;
  },

  async login(credentials) {
    const response = await api.post('/accounts/auth/login/', credentials);
    const { access, refresh } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    return response.data;
  },

  async getProfile() {
    const response = await api.get('/accounts/auth/profile/');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};
```

### Products Service

```javascript
// src/services/productService.js
import api from '../api/axios';

export const productService = {
  async getProducts(params = {}) {
    const response = await api.get('/products/', { params });
    return response.data;
  },

  async getProduct(id) {
    const response = await api.get(`/products/${id}/`);
    return response.data;
  },

  async getCategories() {
    const response = await api.get('/products/categories/');
    return response.data;
  },
};
```

### Cart Service

```javascript
// src/services/cartService.js
import api from '../api/axios';

export const cartService = {
  async getCart() {
    const response = await api.get('/cart/');
    return response.data;
  },

  async addToCart(productId, quantity = 1) {
    const response = await api.post('/cart/items/', {
      product_id: productId,
      quantity,
    });
    return response.data;
  },

  async updateCartItem(itemId, quantity) {
    const response = await api.patch(`/cart/items/${itemId}/`, { quantity });
    return response.data;
  },

  async removeFromCart(itemId) {
    await api.delete(`/cart/items/${itemId}/`);
  },

  async clearCart() {
    await api.delete('/cart/clear/');
  },
};
```

### React Hook Example

```javascript
// src/hooks/useProducts.js
import { useState, useEffect } from 'react';
import { productService } from '../services/productService';

export const useProducts = (filters = {}) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const data = await productService.getProducts(filters);
        setProducts(data.results);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [JSON.stringify(filters)]);

  return { products, loading, error };
};
```

---

## Error Responses

All error responses follow this format:

```javascript
// 400 Bad Request
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}

// 401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}

// 404 Not Found
{
  "detail": "Not found."
}

// 500 Internal Server Error
{
  "detail": "Internal server error."
}
```

---

## Pagination

All list endpoints support pagination:

```javascript
// Request
GET /api/v1/products/?page=2&page_size=20

// Response
{
  "count": 100,
  "next": "http://api.example.com/api/v1/products/?page=3",
  "previous": "http://api.example.com/api/v1/products/?page=1",
  "results": [...]
}
```

---

## Filtering & Search

### Products
- `?search=keyword` - Search in name and description
- `?category=1` - Filter by category ID
- `?min_price=100&max_price=500` - Price range
- `?ordering=-created_at` - Sort by field (prefix `-` for descending)

### Orders
- `?status=pending` - Filter by status
- `?ordering=-created_at` - Sort by date

---

## Payment Methods

Supported payment methods:
- `telebirr` - TeleBirr
- `chapa` - Chapa
- `cbe` - Commercial Bank of Ethiopia

---

## Order Status Values

- `pending` - Order placed, awaiting payment
- `processing` - Payment confirmed, preparing order
- `shipped` - Order shipped
- `delivered` - Order delivered
- `cancelled` - Order cancelled

---

## Rate Limiting

- **Anonymous users:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour

---

## Support

- **API Base URL:** `https://your-app-name.onrender.com`
- **Health Check:** `GET /health/`
- **API Root:** `GET /`

For issues, contact the backend team or check the API logs.
