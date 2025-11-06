# FusionForms Backend API

A robust, production-ready Django REST Framework backend for FusionForms - a modern form builder and submission management platform.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Security](#security)
- [Contributing](#contributing)

## 🎯 Overview

FusionForms Backend is a comprehensive REST API built with Django and Django REST Framework. It provides a complete backend solution for building, managing, and analyzing forms with features including:

- Form creation and management
- Form submissions handling
- Real-time analytics
- Webhook integrations
- User authentication and authorization
- Rate limiting and caching
- Health monitoring

## ✨ Features

### Core Features
- **Form Management**: Create, update, and manage forms with JSON-based schema
- **Form Submissions**: Handle form submissions with validation and spam protection
- **Analytics**: Track form views, submissions, completion rates, and field-level analytics
- **Webhooks**: Configure webhooks to trigger on form events (submissions, views, etc.)
- **User Management**: Role-based access control (Admin, Designer, Analyst, Viewer)
- **Form Themes**: Customize form appearance with themes

### Production Features
- **Rate Limiting**: Configurable rate limits for different endpoints
- **Caching**: Redis-based caching for improved performance
- **Health Checks**: Kubernetes-ready health check endpoints
- **Structured Logging**: JSON logging for production environments
- **Monitoring**: Metrics endpoint for observability
- **Security**: Security headers, CORS, CSRF protection, reCAPTCHA integration
- **API Versioning**: Support for API versioning with backward compatibility
- **Database Indexing**: Optimized database queries with strategic indexes

## 🛠 Tech Stack

### Core Framework
- **Django 4.2.5**: Web framework
- **Django REST Framework 3.14.0**: REST API framework
- **Python 3.11+**: Programming language

### Database & Caching
- **PostgreSQL 15**: Primary database
- **Redis 7**: Caching and Celery message broker

### Task Queue
- **Celery 5.3.1**: Asynchronous task processing

### Additional Libraries
- **psycopg2-binary**: PostgreSQL adapter
- **django-redis**: Redis cache backend
- **django-cors-headers**: CORS handling
- **django-filter**: Advanced filtering
- **drf-spectacular**: OpenAPI 3.0 schema generation
- **Pillow**: Image processing
- **jsonschema**: JSON schema validation
- **python-json-logger**: Structured logging
- **requests**: HTTP client for webhooks

## 🏗 Architecture

### Project Structure

```
backend/
├── apps/
│   ├── accounts/          # User authentication and management
│   ├── forms/             # Form creation and management
│   ├── submissions/       # Form submission handling
│   ├── analytics/         # Analytics and reporting
│   ├── webhooks/          # Webhook management and delivery
│   └── core/              # Shared utilities
│       ├── caching.py     # Cache utilities
│       ├── exceptions.py  # Custom exception handlers
│       ├── health.py      # Health check endpoints
│       ├── middleware.py # Request logging and metrics
│       ├── monitoring.py  # Metrics endpoint
│       ├── permissions.py # Custom permissions (RBAC)
│       └── throttling.py  # Rate limiting
├── fusionforms/           # Django project settings
│   ├── settings.py        # Application settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│   ├── asgi.py           # ASGI configuration
│   └── celery.py         # Celery configuration
├── tests/                 # Test suite
├── logs/                  # Application logs
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
└── gunicorn.conf.py      # Gunicorn configuration
```

### Application Modules

1. **accounts**: User authentication, registration, and role-based access control
2. **forms**: Form CRUD operations, versioning, themes, and public form access
3. **submissions**: Form submission handling, validation, and saved form drafts
4. **analytics**: Form and field-level analytics tracking
5. **webhooks**: Webhook configuration and asynchronous delivery
6. **core**: Shared utilities including caching, permissions, health checks, and monitoring

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 7 or higher
- pip (Python package manager)

### Local Development Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd formfussion/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DB_HOST=localhost
   DB_NAME=fusionforms
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   REDIS_CACHE_URL=redis://localhost:6379/1
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

5. **Set up PostgreSQL database**:
   ```bash
   createdb fusionforms
   ```

6. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Start Redis** (if not running as a service):
   ```bash
   redis-server
   ```

9. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

10. **Start Celery worker** (in a separate terminal):
    ```bash
    celery -A fusionforms worker -l info
    ```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and start services**:
   ```bash
   docker-compose up --build
   ```

2. **Run migrations** (in a separate terminal):
   ```bash
   docker-compose exec api python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

The API will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `DB_HOST` | Database host | `localhost` |
| `DB_NAME` | Database name | `fusionforms` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | Required |
| `DB_PORT` | Database port | `5432` |
| `REDIS_CACHE_URL` | Redis cache URL | `redis://localhost:6379/1` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Celery result backend | `redis://localhost:6379/0` |
| `THROTTLE_RATE_ANON` | Anonymous user rate limit | `60/min` |
| `THROTTLE_RATE_USER` | Authenticated user rate limit | `600/min` |
| `THROTTLE_RATE_SUBMISSIONS` | Submission rate limit | `30/min` |
| `THROTTLE_RATE_AUTH` | Auth endpoint rate limit | `10/min` |
| `THROTTLE_RATE_WEBHOOKS` | Webhook rate limit | `100/min` |
| `RECAPTCHA_SECRET` | reCAPTCHA secret key | Optional |
| `ALLOWED_HOSTS` | Allowed hostnames | `*` (development) |

### Rate Limiting

The API implements configurable rate limiting with the following default scopes:

- **Anonymous users**: 60 requests/minute
- **Authenticated users**: 600 requests/minute
- **Form submissions**: 30 requests/minute
- **Authentication endpoints**: 10 requests/minute
- **Webhook operations**: 100 requests/minute

### Caching

Redis caching is configured with:
- Compression support (zlib)
- Connection pooling
- Timeout handling
- Automatic fallback to local memory cache

## 📚 API Documentation

### Base URL

- **Development**: `http://localhost:8000`
- **API v1**: `http://localhost:8000/api/v1/`
- **API (backward compatible)**: `http://localhost:8000/api/`

### Interactive API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### API Endpoints

#### Authentication (`/api/v1/accounts/`)
- `POST /api/v1/accounts/register/` - User registration
- `POST /api/v1/accounts/login/` - User login
- `POST /api/v1/accounts/logout/` - User logout
- `GET /api/v1/accounts/profile/` - Get user profile
- `PUT /api/v1/accounts/profile/` - Update user profile

#### Forms (`/api/v1/forms/`)
- `GET /api/v1/forms/` - List user's forms
- `POST /api/v1/forms/` - Create a new form
- `GET /api/v1/forms/{id}/` - Get form details
- `PUT /api/v1/forms/{id}/` - Update form
- `PATCH /api/v1/forms/{id}/` - Partially update form
- `DELETE /api/v1/forms/{id}/` - Delete form
- `GET /api/v1/forms/public/{id}/` - Get public form (no auth required)
- `GET /api/v1/forms/themes/` - List form themes
- `POST /api/v1/forms/themes/` - Create form theme

#### Submissions (`/api/v1/submissions/`)
- `GET /api/v1/submissions/` - List submissions
- `POST /api/v1/submissions/` - Submit a form
- `GET /api/v1/submissions/{id}/` - Get submission details
- `DELETE /api/v1/submissions/{id}/` - Delete submission
- `GET /api/v1/submissions/export/` - Export submissions as CSV

#### Analytics (`/api/v1/analytics/`)
- `GET /api/v1/analytics/forms/{form_id}/` - Get form analytics
- `GET /api/v1/analytics/forms/{form_id}/fields/` - Get field-level analytics

#### Webhooks (`/api/v1/webhooks/`)
- `GET /api/v1/webhooks/` - List webhooks
- `POST /api/v1/webhooks/` - Create webhook
- `GET /api/v1/webhooks/{id}/` - Get webhook details
- `PUT /api/v1/webhooks/{id}/` - Update webhook
- `DELETE /api/v1/webhooks/{id}/` - Delete webhook
- `GET /api/v1/webhooks/{id}/logs/` - Get webhook logs

#### Health Checks
- `GET /health/` - Basic health check
- `GET /health/ready/` - Readiness probe (checks DB, cache, Celery)
- `GET /health/live/` - Liveness probe
- `GET /health/metrics/` - Application metrics

### Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Token <your-token>
```

For session-based authentication (browsable API), use Django's session authentication.

## 🗄 Database Models

### User Model
- Extends Django's AbstractUser
- Roles: Admin, Designer, Analyst, Viewer
- Organization field for multi-tenant support

### Form Model
- UUID primary key
- JSON schema for form structure
- Status: Draft, Published, Archived
- Version tracking
- Created/updated timestamps

### Submission Model
- UUID primary key
- JSON data storage
- IP address and user agent tracking
- Spam detection flag
- Timestamps

### Analytics Models
- **FormAnalytics**: Form-level metrics (views, submissions, completion rate)
- **FieldAnalytics**: Field-level metrics (response count, abandonment rate)

### Webhook Models
- **Webhook**: Webhook configuration (URL, events, secret)
- **WebhookLog**: Webhook delivery logs

## 💻 Development

### Running the Development Server

```bash
python manage.py runserver
```

### Running Celery Worker

```bash
celery -A fusionforms worker -l info
```

### Running Celery Beat (for periodic tasks)

```bash
celery -A fusionforms beat -l info
```

### Making Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Code Quality

#### Linting
```bash
# Install flake8 or pylint (if configured)
pip install flake8
flake8 .
```

#### Formatting
```bash
# Install black (if configured)
pip install black
black .
```

## 🧪 Testing

### Running Tests

The project uses Django's built-in test framework. To run tests:

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.forms

# Run tests with verbose output
python manage.py test --verbosity=2

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Structure

Tests should be organized in `tests/` directories within each app:

```
apps/
├── forms/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
```

### Writing Tests

Example test structure:

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.forms.models import Form

User = get_user_model()

class FormModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_form_creation(self):
        form = Form.objects.create(
            title='Test Form',
            owner=self.user,
            schema={'fields': []}
        )
        self.assertEqual(form.title, 'Test Form')
        self.assertEqual(form.owner, self.user)
```

### Test Coverage

Aim for at least 80% test coverage. Focus on:
- Model methods and properties
- View logic and permissions
- Serializer validation
- Business logic in services/utils

## 🚀 Deployment

### Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in environment variables
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching and Celery
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS settings for frontend domain
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up environment-specific settings

### Docker Deployment

#### Build Production Image

```bash
docker build -t fusionforms-backend:latest .
```

#### Run with Docker Compose (Production)

Update `docker-compose.yml` for production:

```yaml
services:
  api:
    build: .
    command: gunicorn -c gunicorn.conf.py fusionforms.wsgi:application
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    # ... other production settings
```

#### Deploy with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Gunicorn Configuration

The project includes `gunicorn.conf.py` with production-ready settings:
- Worker count: `(CPU cores * 2) + 1`
- Thread-based workers for I/O-bound operations
- Graceful timeout handling
- Access and error logging

### Environment Variables for Production

```bash
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_HOST=<production-db-host>
DB_NAME=fusionforms
DB_USER=<db-user>
DB_PASSWORD=<strong-password>
REDIS_CACHE_URL=redis://<redis-host>:6379/1
CELERY_BROKER_URL=redis://<redis-host>:6379/0
CELERY_RESULT_BACKEND=redis://<redis-host>:6379/0
RECAPTCHA_SECRET=<recaptcha-secret>
```

### Database Migrations in Production

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Kubernetes Deployment

The health check endpoints are Kubernetes-ready:

- **Liveness Probe**: `GET /health/live/`
- **Readiness Probe**: `GET /health/ready/`

Example Kubernetes configuration:

```yaml
livenessProbe:
  httpGet:
    path: /health/live/
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready/
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints

- **`GET /health/`**: Basic health check
  - Returns: `{"status": "ok"}`

- **`GET /health/ready/`**: Readiness probe
  - Checks: Database, Redis cache, Celery connection
  - Returns: `{"status": "ready"}` or error details

- **`GET /health/live/`**: Liveness probe
  - Returns: `{"status": "alive"}`

- **`GET /health/metrics/`**: Application metrics
  - Returns: Request counts, response times, cache stats, database stats

### Monitoring Integration

The metrics endpoint is compatible with Prometheus:

```bash
# Scrape metrics
curl http://localhost:8000/health/metrics/
```

### Logging

Structured JSON logging is configured for production:

- Logs are written to `logs/fusionforms.log`
- JSON format for easy parsing by log aggregation tools
- Request/response logging via middleware
- Error logging with stack traces

### Request Metrics

The API includes request timing headers:
- `X-Request-ID`: Unique request identifier
- `X-Response-Time`: Response time in milliseconds

## 🔒 Security

### Security Features

- **CSRF Protection**: Enabled for state-changing operations
- **CORS**: Configurable CORS headers for cross-origin requests
- **Security Headers**: X-Frame-Options, Content-Security-Policy
- **Rate Limiting**: Protection against brute force and DDoS
- **Token Authentication**: Secure token-based authentication
- **Password Validation**: Django's password validators
- **reCAPTCHA**: Optional spam protection for form submissions
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Django templates escape by default

### Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Use HTTPS**: Always use SSL/TLS in production
3. **Keep dependencies updated**: Regularly update packages
4. **Review permissions**: Ensure proper RBAC implementation
5. **Monitor logs**: Watch for suspicious activity
6. **Regular backups**: Backup database regularly
7. **Rate limiting**: Configure appropriate rate limits

### CORS Configuration

Configure CORS in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## 🤝 Contributing

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow PEP 8 style guide
   - Write tests for new features
   - Update documentation

3. **Run tests**:
   ```bash
   python manage.py test
   ```

4. **Commit changes**:
   ```bash
   git commit -m "Add: description of changes"
   ```

5. **Push and create pull request**

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Write docstrings for classes and functions
- Keep functions focused and small
- Use meaningful variable names

### Pull Request Guidelines

- Include tests for new features
- Update documentation if needed
- Ensure all tests pass
- Request review from maintainers

## 📝 License

[Add your license information here]

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review API documentation at `/api/docs/`

## 🔗 Related Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)