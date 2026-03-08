# API Documentation

Complete reference for all API endpoints and data structures.

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
  - [Users](#users)
  - [Products](#products)
  - [Orders](#orders)
- [Data Types](#data-types)
- [Rate Limiting](#rate-limiting)

## Base URL

```
https://api.example.com/v1
```

All requests should be made to this base URL. The API only accepts HTTPS requests.

## Authentication

Authentication is required for all endpoints using API key authentication.

### API Key Authentication

Include your API key in the `Authorization` header:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/users
```

**Getting Your API Key:**

1. Log in to your account
2. Go to Settings → API Keys
3. Click "Generate New Key"
4. Copy and store securely

### Rate Limiting

Rate limits are enforced per API key:

- **Rate Limit**: 1000 requests per hour
- **Burst Limit**: 100 requests per minute
- **Headers**: Check `X-RateLimit-*` response headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Error Handling

All errors return JSON with status code and error details.

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `SERVER_ERROR` | 500 | Internal server error |

---

## Endpoints

### Users

#### List Users

Retrieve a paginated list of all users.

```
GET /users
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1) |
| `limit` | integer | No | Items per page (default: 20, max: 100) |
| `status` | string | No | Filter by status: `active`, `inactive`, `banned` |
| `search` | string | No | Search by name or email |
| `sort` | string | No | Sort field: `created_at`, `name` (prefix with `-` for descending) |

**Response:**

```json
{
  "data": [
    {
      "id": "usr_123",
      "name": "John Doe",
      "email": "john@example.com",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

**Example:**

```bash
# Get active users, page 2
curl "https://api.example.com/v1/users?status=active&page=2&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Get User by ID

Retrieve a specific user by their ID.

```
GET /users/{id}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | User ID |

**Response:**

```json
{
  "data": {
    "id": "usr_123",
    "name": "John Doe",
    "email": "john@example.com",
    "status": "active",
    "role": "user",
    "profile": {
      "bio": "Software developer",
      "avatar_url": "https://example.com/avatar.jpg",
      "location": "New York"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:22:00Z"
  }
}
```

**Errors:**

- `404 NOT_FOUND` - User does not exist

**Example:**

```bash
curl https://api.example.com/v1/users/usr_123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Create User

Create a new user account.

```
POST /users
```

**Request Body:**

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "secure_password",
  "role": "user"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | Yes | Length: 1-255 characters |
| `email` | string | Yes | Valid email format, unique |
| `password` | string | Yes | Minimum 8 characters |
| `role` | string | No | Default: `user`, values: `user`, `admin` |

**Response:**

```json
{
  "data": {
    "id": "usr_456",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "user",
    "created_at": "2024-01-25T09:15:00Z"
  }
}
```

**Errors:**

- `400 VALIDATION_ERROR` - Invalid data
- `409 CONFLICT` - Email already exists

**Example:**

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "secure_password"
  }'
```

#### Update User

Update an existing user.

```
PATCH /users/{id}
```

**Request Body:**

Only include fields you want to update:

```json
{
  "name": "Jane Doe",
  "profile": {
    "bio": "Updated bio"
  }
}
```

**Response:**

Same as Get User response.

**Errors:**

- `404 NOT_FOUND` - User does not exist
- `400 VALIDATION_ERROR` - Invalid data

#### Delete User

Delete a user account.

```
DELETE /users/{id}
```

**Response:**

```json
{
  "data": {
    "success": true,
    "message": "User deleted successfully"
  }
}
```

**Errors:**

- `404 NOT_FOUND` - User does not exist

---

### Products

#### List Products

```
GET /products
```

Query parameters similar to users endpoint. Additional filters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category ID |
| `min_price` | number | Minimum price filter |
| `max_price` | number | Maximum price filter |
| `in_stock` | boolean | Only show in-stock items |

---

### Orders

#### Create Order

```
POST /orders
```

**Request Body:**

```json
{
  "user_id": "usr_123",
  "items": [
    {
      "product_id": "prod_456",
      "quantity": 2
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  }
}
```

---

## Data Types

### User Object

```typescript
interface User {
  /** Unique user identifier */
  id: string;
  /** Full name */
  name: string;
  /** Email address */
  email: string;
  /** User status: active, inactive, banned */
  status: "active" | "inactive" | "banned";
  /** User role: user, admin */
  role: "user" | "admin";
  /** User profile information */
  profile?: {
    bio?: string;
    avatar_url?: string;
    location?: string;
  };
  /** Account creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string;
}
```

### Product Object

```typescript
interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category_id: string;
  in_stock: boolean;
  stock_count: number;
  created_at: string;
  updated_at: string;
}
```

### Error Object

```typescript
interface Error {
  error: {
    code: string;
    message: string;
    details?: Array<{
      field: string;
      message: string;
    }>;
  };
}
```

---

## Webhooks

Subscribe to events via webhooks.

### Event Types

- `user.created` - New user registered
- `user.updated` - User profile updated
- `order.created` - New order placed
- `order.completed` - Order shipped

### Webhook Format

```json
{
  "id": "evt_123",
  "type": "user.created",
  "timestamp": "2024-01-25T10:30:00Z",
  "data": {
    "id": "usr_456",
    "name": "Jane Smith",
    "email": "jane@example.com"
  }
}
```

---

## SDK Examples

### JavaScript

```javascript
import { ApiClient } from '@example/sdk';

const client = new ApiClient({
  apiKey: process.env.API_KEY,
});

const users = await client.users.list({ limit: 50 });
const user = await client.users.get('usr_123');
```

### Python

```python
from example_sdk import ApiClient

client = ApiClient(api_key=os.environ['API_KEY'])

users = client.users.list(limit=50)
user = client.users.get('usr_123')
```

---

## Best Practices

- Always store API keys securely (use environment variables)
- Use HTTPS only
- Implement exponential backoff for retries
- Cache responses when appropriate
- Monitor rate limit headers
- Validate webhook signatures

---

## Support

For API support:

- Email: api-support@example.com
- Slack: [Join Channel](https://slack.example.com)
- Documentation: [https://docs.example.com](https://docs.example.com)
