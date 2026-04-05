# CampusConnect Mini-Ecommerce API

A professional e-commerce REST API built with Django and Django REST Framework for campus marketplace applications.

---

## 🚀 Quick Start

### API Base URL
```
Production: https://campus-ecommerce-api.onrender.com/api/v1
Health Check: https://campus-ecommerce-api.onrender.com/health/
```

### Authentication
JWT Bearer Token - Include in request headers:
```
Authorization: Bearer <your_access_token>
```

---

## 📋 Core Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/accounts/auth/register/` | POST | Register new user |
| `/api/v1/accounts/auth/login/` | POST | Login and get JWT tokens |
| `/api/v1/accounts/auth/token/refresh/` | POST | Refresh access token |
| `/api/v1/accounts/auth/profile/` | GET | Get user profile |

### Products
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/products/` | GET | List all products |
| `/api/v1/products/{id}/` | GET | Get product details |
| `/api/v1/products/categories/` | GET | List categories |

### Cart
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/cart/` | GET | Get user's cart |
| `/api/v1/cart/items/` | POST | Add item to cart |
| `/api/v1/cart/items/{id}/` | PATCH | Update cart item |
| `/api/v1/cart/items/{id}/` | DELETE | Remove from cart |

### Orders
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/orders/` | GET | List user's orders |
| `/api/v1/orders/` | POST | Create new order |
| `/api/v1/orders/{id}/` | GET | Get order details |

### Additional Features
- `/api/v1/reviews/` - Product reviews
- `/api/v1/wishlist/` - User wishlist
- `/api/v1/notifications/` - User notifications
- `/api/v1/vendors/` - Vendor management
- `/api/v1/payments/` - Payment processing
- `/api/v1/chat/` - Messaging system

📖 **Complete API Reference:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🛠️ Tech Stack

- **Framework:** Django 6.0.3
- **API:** Django REST Framework 3.17.1
- **Authentication:** JWT (djangorestframework-simplejwt 5.5.1)
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Server:** Gunicorn 21.2.0
- **Static Files:** WhiteNoise 6.12.0
- **CORS:** django-cors-headers 4.9.0

---

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd Mini-Ecommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start server**
   ```bash
   python manage.py runserver
   ```

7. **Access API**
   - API Root: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Health: http://localhost:8000/health/

---

## 🌐 React Integration

### Install Axios
```bash
npm install axios
```

### Setup API Client
```javascript
// src/api/client.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-app-name.onrender.com/api/v1',
  headers: { 'Content-Type': 'application/json' }
});

// Auto-attach JWT token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
```

### Authentication Example
```javascript
import api from './api/client';

// Register
const register = async (userData) => {
  const response = await api.post('/accounts/auth/register/', userData);
  return response.data;
};

// Login
const login = async (username, password) => {
  const response = await api.post('/accounts/auth/login/', { username, password });
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  return response.data;
};

// Get Products
const getProducts = async () => {
  const response = await api.get('/products/');
  return response.data.results;
};

// Add to Cart
const addToCart = async (productId, quantity = 1) => {
  const response = await api.post('/cart/items/', { 
    product_id: productId, 
    quantity 
  });
  return response.data;
};
```

📖 **Complete React Guide:** [FRONTEND_QUICKSTART.md](./FRONTEND_QUICKSTART.md)

---

## 🚀 Deployment (Render.com)

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy CampusConnect Mini-Ecommerce"
   git push origin main
   ```

2. **On Render Dashboard**
   - New → Blueprint
   - Connect GitHub repository
   - Render auto-detects `render.yaml`

3. **Set Environment Variables**
   ```bash
   DATABASE_URL=<auto-set-by-render>
   SECRET_KEY=<generate-new-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.com
   ```

4. **Create Superuser** (via Render Shell)
   ```bash
   python manage.py createsuperuser
   ```

### Environment Variables

**Required:**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
```

**Optional (Payment Gateways):**
```bash
TELEBIRR_MERCHANT_ID=your_id
TELEBIRR_API_KEY=your_key
CHAPA_SECRET_KEY=your_key
CBE_MERCHANT_CODE=your_code
CBE_API_KEY=your_key
```

**Optional (CORS):**
```bash
CORS_ALLOWED_ORIGINS=https://frontend.com,http://localhost:3000
```

See `.env.example` for complete template.

---

## 📁 Project Structure

```
Mini-Ecommerce/
├── apps/
│   ├── accounts/       # User authentication & profiles
│   ├── cart/          # Shopping cart
│   ├── chat/          # Messaging
│   ├── core/          # Shared utilities
│   ├── notifications/ # Notifications
│   ├── orders/        # Order management
│   ├── payments/      # Payment processing
│   ├── products/      # Product catalog
│   ├── reviews/       # Product reviews
│   ├── vendors/       # Vendor management
│   └── wishlist/      # User wishlists
├── MiniEcommerce/     # Project settings
├── requirements.txt   # Dependencies
├── build.sh          # Build script
├── render.yaml       # Deployment config
└── manage.py         # Django CLI
```

---

## 🔐 Security Features

- ✅ JWT authentication with token refresh
- ✅ HTTPS enforced in production
- ✅ Secure cookies (session & CSRF)
- ✅ CORS protection
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection
- ✅ Environment-based secrets
- ✅ HSTS headers

---

## 📊 API Features

- ✅ RESTful design
- ✅ JWT authentication
- ✅ Pagination (10 items per page)
- ✅ Filtering & search
- ✅ Ordering/sorting
- ✅ CORS enabled
- ✅ Comprehensive error handling
- ✅ Health check endpoint

---

## 🧪 Testing

### Health Check
```bash
curl https://your-app-name.onrender.com/health/
```

### Register User
```bash
curl -X POST https://your-app-name.onrender.com/api/v1/accounts/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### Login
```bash
curl -X POST https://your-app-name.onrender.com/api/v1/accounts/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Get Products
```bash
curl https://your-app-name.onrender.com/api/v1/products/
```

---

## 📚 Documentation

- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference with examples
- **[FRONTEND_QUICKSTART.md](./FRONTEND_QUICKSTART.md)** - React integration guide
- **[.env.example](./.env.example)** - Environment variables template

---

## 🐛 Troubleshooting

### CORS Errors
Add your frontend domain to `CORS_ALLOWED_ORIGINS` environment variable.

### Authentication Errors
- Verify token is included in Authorization header
- Check token hasn't expired (60 minutes)
- Use refresh token to get new access token

### 404 Errors
- Verify endpoint URL includes `/api/v1/` prefix
- Check trailing slashes in URLs

---

## 📞 Support

- **Health Check:** `GET /health/`
- **API Root:** `GET /` (lists all endpoints)
- **Admin Panel:** `/admin/`

---

## 📝 License

MIT License

---

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

**CampusConnect Mini-Ecommerce** - Professional E-commerce API for Campus Marketplaces
