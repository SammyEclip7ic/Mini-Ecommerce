# Frontend Quick Start Guide

**For React Developers integrating with CampusConnect Mini-Ecommerce API**

---

## 🎯 Essential Information

### API Base URL
```
https://your-app-name.onrender.com/api/v1
```

### Authentication Type
JWT Bearer Token

### CORS
Enabled - Your frontend domain must be added to `CORS_ALLOWED_ORIGINS`

---

## ⚡ 5-Minute Integration

### 1. Install Axios
```bash
npm install axios
```

### 2. Create API Client (`src/api/client.js`)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-app-name.onrender.com/api/v1',
  headers: { 'Content-Type': 'application/json' }
});

// Auto-attach token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
```

### 3. Authentication (`src/services/auth.js`)
```javascript
import api from '../api/client';

export const auth = {
  // Register
  register: (data) => api.post('/accounts/auth/register/', data),
  
  // Login
  login: async (username, password) => {
    const { data } = await api.post('/accounts/auth/login/', { username, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  },
  
  // Get Profile
  getProfile: () => api.get('/accounts/auth/profile/'),
  
  // Logout
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};
```

### 4. Products (`src/services/products.js`)
```javascript
import api from '../api/client';

export const products = {
  getAll: (params) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}/`),
  getCategories: () => api.get('/products/categories/')
};
```

### 5. Cart (`src/services/cart.js`)
```javascript
import api from '../api/client';

export const cart = {
  get: () => api.get('/cart/'),
  add: (productId, quantity = 1) => 
    api.post('/cart/items/', { product_id: productId, quantity }),
  update: (itemId, quantity) => 
    api.patch(`/cart/items/${itemId}/`, { quantity }),
  remove: (itemId) => api.delete(`/cart/items/${itemId}/`),
  clear: () => api.delete('/cart/clear/')
};
```

---

## 🔑 Common Endpoints

| Action | Endpoint | Method | Auth |
|--------|----------|--------|------|
| Register | `/accounts/auth/register/` | POST | No |
| Login | `/accounts/auth/login/` | POST | No |
| Profile | `/accounts/auth/profile/` | GET | Yes |
| Products | `/products/` | GET | No |
| Product Detail | `/products/{id}/` | GET | No |
| Cart | `/cart/` | GET | Yes |
| Add to Cart | `/cart/items/` | POST | Yes |
| Orders | `/orders/` | GET/POST | Yes |
| Reviews | `/reviews/` | GET/POST | Yes* |
| Wishlist | `/wishlist/` | GET | Yes |

*POST requires authentication

---

## 📝 Request Examples

### Register User
```javascript
const registerUser = async () => {
  try {
    const response = await api.post('/accounts/auth/register/', {
      username: 'john_doe',
      email: 'john@example.com',
      password: 'securePass123',
      first_name: 'John',
      last_name: 'Doe'
    });
    console.log('User registered:', response.data);
  } catch (error) {
    console.error('Registration failed:', error.response.data);
  }
};
```

### Login
```javascript
const login = async () => {
  try {
    const response = await api.post('/accounts/auth/login/', {
      username: 'john_doe',
      password: 'securePass123'
    });
    
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    
    console.log('Login successful');
  } catch (error) {
    console.error('Login failed:', error.response.data);
  }
};
```

### Get Products with Filters
```javascript
const getProducts = async () => {
  try {
    const response = await api.get('/products/', {
      params: {
        search: 'laptop',
        category: 1,
        min_price: 100,
        max_price: 1000,
        ordering: '-created_at',
        page: 1
      }
    });
    
    console.log('Products:', response.data.results);
    console.log('Total:', response.data.count);
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
};
```

### Add to Cart
```javascript
const addToCart = async (productId) => {
  try {
    const token = localStorage.getItem('access_token');
    
    const response = await api.post('/cart/items/', 
      { product_id: productId, quantity: 1 },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    console.log('Added to cart:', response.data);
  } catch (error) {
    console.error('Failed to add to cart:', error.response.data);
  }
};
```

### Create Order
```javascript
const createOrder = async () => {
  try {
    const response = await api.post('/orders/', {
      shipping_address: {
        street: 'Bole Road',
        city: 'Addis Ababa',
        state: 'Addis Ababa',
        postal_code: '1000',
        country: 'Ethiopia'
      },
      payment_method: 'telebirr'
    });
    
    console.log('Order created:', response.data);
  } catch (error) {
    console.error('Order failed:', error.response.data);
  }
};
```

---

## 🎣 React Hooks

### useAuth Hook
```javascript
import { useState, useEffect } from 'react';
import { auth } from '../services/auth';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const { data } = await auth.getProfile();
          setUser(data);
        } catch (error) {
          auth.logout();
        }
      }
      setLoading(false);
    };
    loadUser();
  }, []);

  return { user, loading, setUser };
};
```

### useProducts Hook
```javascript
import { useState, useEffect } from 'react';
import { products } from '../services/products';

export const useProducts = (filters = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await products.getAll(filters);
        setData(response.data.results);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [JSON.stringify(filters)]);

  return { data, loading, error };
};
```

### useCart Hook
```javascript
import { useState, useEffect } from 'react';
import { cart } from '../services/cart';

export const useCart = () => {
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchCart = async () => {
    try {
      const { data } = await cart.get();
      setCartData(data);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const addItem = async (productId, quantity) => {
    await cart.add(productId, quantity);
    await fetchCart();
  };

  const updateItem = async (itemId, quantity) => {
    await cart.update(itemId, quantity);
    await fetchCart();
  };

  const removeItem = async (itemId) => {
    await cart.remove(itemId);
    await fetchCart();
  };

  return { cartData, loading, addItem, updateItem, removeItem };
};
```

---

## 🔄 Token Refresh

### Auto-refresh expired tokens
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-app-name.onrender.com/api/v1'
});

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const { data } = await axios.post(
          'https://your-app-name.onrender.com/api/v1/accounts/auth/token/refresh/',
          { refresh: refreshToken }
        );

        localStorage.setItem('access_token', data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        
        return api(originalRequest);
      } catch (err) {
        localStorage.clear();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);
```

---

## ⚠️ Common Issues

### CORS Error
**Problem:** `Access-Control-Allow-Origin` error  
**Solution:** Contact backend team to add your domain to `CORS_ALLOWED_ORIGINS`

### 401 Unauthorized
**Problem:** Token expired or missing  
**Solution:** Check token exists and implement token refresh

### 404 Not Found
**Problem:** Wrong endpoint URL  
**Solution:** Verify endpoint path and include `/api/v1/` prefix

---

## 📦 Response Formats

### Success (Single Object)
```json
{
  "id": 1,
  "name": "Product Name",
  "price": "99.99"
}
```

### Success (List with Pagination)
```json
{
  "count": 100,
  "next": "https://api.example.com/api/v1/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error
```json
{
  "username": ["This field is required."],
  "email": ["Enter a valid email address."]
}
```

---

## 🔍 Query Parameters

### Products
```javascript
// Search
?search=laptop

// Filter by category
?category=1

// Price range
?min_price=100&max_price=500

// Sort
?ordering=-created_at  // newest first
?ordering=price        // cheapest first

// Pagination
?page=2&page_size=20
```

---

## 📱 Example React Component

```javascript
import React, { useEffect, useState } from 'react';
import api from './api/client';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await api.get('/products/');
        setProducts(data.results);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleAddToCart = async (productId) => {
    try {
      await api.post('/cart/items/', {
        product_id: productId,
        quantity: 1
      });
      alert('Added to cart!');
    } catch (error) {
      alert('Failed to add to cart');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>${product.price}</p>
          <button onClick={() => handleAddToCart(product.id)}>
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}

export default ProductList;
```

---

## 📚 Full Documentation

For complete API reference, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## ✅ Checklist

- [ ] Install axios
- [ ] Create API client with base URL
- [ ] Implement authentication (login/register)
- [ ] Store JWT tokens in localStorage
- [ ] Add Authorization header to requests
- [ ] Implement token refresh logic
- [ ] Handle error responses
- [ ] Test all endpoints
- [ ] Request CORS access for your domain

---

**Need Help?** Check the full [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) or contact the backend team.
