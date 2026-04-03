# CampusConnect Mini E-Commerce Platform

A production-ready, scalable backend system for a campus-based multi-vendor e-commerce platform built with Django REST Framework.

## 🎯 Project Overview

CampusConnect Market enables students and local vendors within a university campus to:

- Buy and sell products
- Manage vendor stores
- Place and track orders
- Make secure payments using Ethiopian payment systems (Telebirr, Chapa, CBE)
- Review products and vendors
- Manage wishlists and receive notifications

## 🏗️ Architecture

### Tech Stack

- **Backend Framework**: Django 6.0.3
- **API Framework**: Django REST Framework 3.17.1
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Payment Gateways**: Telebirr, Chapa, CBE
- **Image Handling**: Pillow

### Design Principles

- **SOLID Principles**: Clean, maintainable code
- **Service Layer Architecture**: Business logic separated from views
- **Transaction Safety**: Atomic operations for critical flows
- **Security First**: Role-based access control, JWT authentication
- **Performance Optimized**: Query optimization with select_related/prefetch_related

## 📁 Project Structure

```
Mini-Ecommerce/
├── apps/
│   ├── core/              # Base models, permissions, pagination, utilities
│   ├── accounts/          # User authentication & management
│   ├── vendors/           # Vendor profiles & dashboard
│   ├── products/          # Product & category management
│   ├── cart/              # Shopping cart functionality
│   ├── orders/            # Order processing & management
│   ├── payments/          # Payment gateway integration
│   ├── reviews/           # Product & vendor reviews
│   ├── wishlist/          # User wishlist management
│   ├── notifications/     # Event-driven notifications
│   └── chat/              # Messaging system
├── MiniEcommerce/         # Project settings & configuration
└── media/                 # User-uploaded files
```

## 🚀 Features

### User Management (accounts)

- User registration with role selection (customer/vendor/admin)
- JWT-based authentication
- Role-based permissions
- User profile management

### Vendor Management (vendors)

- Vendor profile creation and management
- Admin approval system
- Vendor dashboard with analytics:
  - Total products
  - Total orders
  - Revenue tracking
  - Recent orders
- Vendor rating system

### Product Management (products)

- CRUD operations for products
- Category management
- Multiple image uploads per product
- Stock management
- Search and filtering
- Product ratings and reviews
- Vendor-specific product listings

### Shopping Cart (cart)

- Persistent cart per user
- Add/update/remove items
- Stock validation
- Real-time price calculation
- Cart totals and item counts

### Order Management (orders)

- Create orders from cart
- Order status lifecycle:
  - pending → paid → processing → shipped → delivered
- Price snapshot at purchase time
- Stock reduction on order placement
- Order history
- Order cancellation (with stock restoration)

### Payment System (payments)

- **Unified Payment Service** with multiple gateways:
  - Cash on Delivery
  - Telebirr
  - Chapa
  - Commercial Bank of Ethiopia (CBE)
- Payment initialization and verification
- Webhook handling for payment callbacks
- Transaction reference tracking
- Payment status management
- One payment per order constraint

### Reviews & Ratings (reviews)

- Product reviews (verified buyers only)
- Vendor ratings
- One review per product per user
- Rating aggregation and statistics
- Review verification based on purchase history

### Wishlist (wishlist)

- Add/remove products
- No duplicates
- User-specific wishlist
- Product details in wishlist

### Notifications (notifications)

- Event-driven notification system
- Notification types:
  - Order placed
  - Payment success/failure
  - Vendor approval/rejection
  - Order status updates
- Mark as read functionality
- Unread count tracking

## 🔐 Security Features

### Authentication & Authorization

- JWT token-based authentication
- Role-based access control (Customer, Vendor, Admin)
- Permission classes:
  - IsCustomer
  - IsVendor
  - IsAdmin
  - IsOwner
  - IsVendorOwner

### Data Protection

- Password hashing
- UUID primary keys
- Input validation
- SQL injection prevention (ORM)
- CSRF protection

## 📊 Database Schema

### Core Models

- **BaseModel**: Abstract model with UUID, timestamps
- **SoftDeleteModel**: Abstract model with soft delete support

### Key Relationships

```
User (1) ─── (1) Vendor
User (1) ─── (1) Cart
User (1) ─── (N) Orders
User (1) ─── (N) Wishlist
User (1) ─── (N) Notifications

Vendor (1) ─── (N) Products
Product (1) ─── (N) ProductImages
Product (1) ─── (N) Reviews
Product (N) ─── (1) Category

Cart (1) ─── (N) CartItems
Order (1) ─── (N) OrderItems
Order (1) ─── (1) Payment

OrderItem (N) ─── (1) Vendor
OrderItem (N) ─── (1) Product
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- pip
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd Mini-Ecommerce
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
   Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Payment Gateway Credentials
TELEBIRR_API_URL=https://api.telebirr.com
TELEBIRR_MERCHANT_ID=your_merchant_id
TELEBIRR_API_KEY=your_api_key

CHAPA_API_URL=https://api.chapa.co/v1
CHAPA_SECRET_KEY=your_secret_key

CBE_API_URL=https://api.cbe.com.et
CBE_MERCHANT_CODE=your_merchant_code
CBE_API_KEY=your_api_key
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Run development server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📡 API Endpoints

### Authentication

```
POST   /api/v1/accounts/auth/register/          # Register new user
POST   /api/v1/accounts/auth/login/             # Login (get JWT tokens)
POST   /api/v1/accounts/auth/token/refresh/     # Refresh access token
GET    /api/v1/accounts/auth/profile/           # Get user profile
```

### Vendors

```
GET    /api/v1/vendors/                          # List approved vendors
POST   /api/v1/vendors/                          # Create vendor profile
GET    /api/v1/vendors/{id}/                     # Get vendor details
PATCH  /api/v1/vendors/{id}/                     # Update vendor profile
GET    /api/v1/vendors/my_profile/               # Get own vendor profile
GET    /api/v1/vendors/dashboard/                # Vendor dashboard stats
POST   /api/v1/vendors/{id}/approve/             # Approve vendor (admin)
POST   /api/v1/vendors/{id}/reject/              # Reject vendor (admin)
```

### Products

```
GET    /api/v1/products/                         # List products
POST   /api/v1/products/                         # Create product (vendor)
GET    /api/v1/products/{slug}/                  # Get product details
PATCH  /api/v1/products/{slug}/                  # Update product (owner)
DELETE /api/v1/products/{slug}/                  # Delete product (owner)
GET    /api/v1/products/my_products/             # Vendor's products
POST   /api/v1/products/{slug}/toggle_active/    # Toggle product status
```

### Categories

```
GET    /api/v1/products/categories/              # List categories
POST   /api/v1/products/categories/              # Create category (admin)
GET    /api/v1/products/categories/{slug}/       # Get category details
```

### Cart

```
GET    /api/v1/cart/                             # Get user's cart
POST   /api/v1/cart/add_item/                    # Add item to cart
PATCH  /api/v1/cart/update-item/{id}/            # Update cart item
DELETE /api/v1/cart/remove-item/{id}/            # Remove cart item
DELETE /api/v1/cart/clear/                       # Clear cart
```

### Orders

```
GET    /api/v1/orders/                           # List user's orders
GET    /api/v1/orders/{id}/                      # Get order details
POST   /api/v1/orders/checkout/                  # Create order from cart
POST   /api/v1/orders/{id}/cancel/               # Cancel order
```

### Payments

```
GET    /api/v1/payments/                         # List user's payments
GET    /api/v1/payments/{id}/                    # Get payment details
POST   /api/v1/payments/initialize/              # Initialize payment
POST   /api/v1/payments/{id}/verify/             # Verify payment
POST   /api/v1/payments/webhook/{method}/        # Payment webhook
```

### Reviews

```
GET    /api/v1/reviews/products/                 # List product reviews
POST   /api/v1/reviews/products/                 # Create product review
GET    /api/v1/reviews/products/{id}/            # Get review details
GET    /api/v1/reviews/products/my_reviews/      # User's reviews
GET    /api/v1/reviews/products/product/{id}/stats/  # Product review stats
```

### Wishlist

```
GET    /api/v1/wishlist/                         # Get user's wishlist
POST   /api/v1/wishlist/                         # Add to wishlist
DELETE /api/v1/wishlist/{id}/                    # Remove from wishlist
DELETE /api/v1/wishlist/clear/                   # Clear wishlist
```

### Notifications

```
GET    /api/v1/notifications/                    # List notifications
GET    /api/v1/notifications/{id}/               # Get notification
POST   /api/v1/notifications/{id}/mark_as_read/  # Mark as read
POST   /api/v1/notifications/mark_all_as_read/   # Mark all as read
GET    /api/v1/notifications/unread_count/       # Get unread count
```

## 🔄 Payment Flow

### 1. Checkout Process

```
User adds items to cart
  ↓
User initiates checkout
  ↓
System creates order (status: pending)
  ↓
System creates payment record
  ↓
System initializes payment with gateway
  ↓
User redirected to payment gateway (if online)
  ↓
User completes payment
  ↓
Gateway sends webhook callback
  ↓
System verifies payment
  ↓
Order status updated to 'paid'
  ↓
Notification sent to user
```

### 2. Payment Methods

#### Cash on Delivery

- No gateway initialization required
- Payment marked as pending
- Completed upon delivery

#### Online Payments (Telebirr, Chapa, CBE)

- Gateway initialization
- Redirect to payment page
- Webhook verification
- Automatic status update

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Test Coverage

- Model validation
- API endpoints
- Permission checks
- Payment flow
- Order creation
- Stock management

## 📈 Performance Optimization

### Database Optimization

- Indexed fields for faster queries
- `select_related()` for foreign keys
- `prefetch_related()` for reverse relations
- Query result caching

### API Optimization

- Pagination on all list endpoints
- Filtering and search capabilities
- Lightweight serializers for list views
- Detailed serializers for detail views

## 🔧 Configuration

### Settings

Key settings in `MiniEcommerce/settings.py`:

- `AUTH_USER_MODEL`: Custom user model
- `REST_FRAMEWORK`: DRF configuration
- `SIMPLE_JWT`: JWT settings
- Payment gateway credentials

### Media Files

- Product images: `media/products/`
- Vendor logos: `media/vendors/logos/`
- Category images: `media/categories/`

## 🚦 Status Codes

- `200 OK`: Successful GET, PATCH, PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## 👥 User Roles

### Customer

- Browse products
- Manage cart
- Place orders
- Make payments
- Write reviews
- Manage wishlist

### Vendor

- Create vendor profile
- Manage products
- View orders
- Access dashboard
- View analytics

### Admin

- Full system access
- Approve/reject vendors
- Manage all resources
- View all orders and payments

## 📝 License

This project is part of a capstone project for AASTU.

## 🤝 Contributing

This is a capstone project. For any issues or suggestions, please contact the development team.

## 📞 Support

For support and queries, please refer to the project documentation or contact the development team.

---

**Built with ❤️ for AASTU Campus Community**
