# Architecture Overview

This backend follows a layered architecture to separate concerns and keep the codebase maintainable:

- **FastAPI** handles routing, request validation, and dependency injection
- **SQLAlchemy ORM** manages database models and relationships
- **Alembic** handles schema migrations
- **PostgreSQL** serves as the primary database
- **External services** (Stripe, SendGrid, AWS S3) are integrated via service modules
- The API is designed to be consumed by a single-page React frontend.

# Core Technologies

- **FastAPI** — high-performance Python web framework
- **SQLAlchemy** — ORM for database interactions
- **Alembic** — database migrations
- **PostgreSQL** — relational database
- **Stripe API** — secure checkout and payment processing
- **SendGrid API** — contact form email delivery
- **AWS S3** — product image storage
- **Pytest** — automated testing

# Project Structure (High-Level)

```
.
├── alembic/            # Database migrations
├── app/
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── routes/         # API route definitions
│   ├── services/       # Stripe, SendGrid, S3 integrations
│   ├── core/           # Config, database session, security helpers
│   └── main.py         # FastAPI app entry point
├── tests/              # Pytest test suite
├── seed.py             # Optional database seeding
├── seed_images.py      # Optional S3 image seeding
└── requirements.txt
```

# Authentication & Authorization (Admin Access)

Admin functionality is restricted to authenticated users.

- Admin users are stored in the database
- Credentials are validated server-side
- Protected routes check admin authentication before allowing access
- The frontend conditionally exposes admin-only UI based on authentication state

This prevents unauthorized users from accessing inventory management and analytics endpoints.

# Stripe Checkout Integration

Stripe is used to securely process customer payments.

## How It Works

- The frontend sends cart data to the backend checkout endpoint
- The backend creates a Stripe Checkout Session using the Stripe Secret Key
- Stripe handles payment processing and redirects the user
- After payment, the user is redirected back to the frontend using FRONTEND_URL

### Required Environment Variables

- `STRIPE_SECRET_KEY`
- `FRONTEND_URL`

Sensitive payment logic is handled exclusively on the backend for security.

# Email Integration (SendGrid)

The contact form submits messages to the backend, which sends emails using SendGrid.

## Flow

- User submits the contact form on the frontend
- Frontend sends the message to the API
- Backend sends an email via SendGrid
- Email is delivered to the configured destination inbox

### Required Environment Variables

- `SENDGRID_API_KEY`
- `FROM_EMAIL`
- `TO_EMAIL`

This keeps email credentials secure and avoids exposing API keys to the client.

# Image Upload & Storage (AWS S3)

Product images are uploaded to and served from AWS S3.

## Key Features

- Images are uploaded from the backend
- Only image keys/URLs are stored in the database
- Images can be added or removed when products or variants change

This approach avoids storing binary files in the database and improves scalability.

# Error Handling & Validation

- Request validation is handled using Pydantic schemas
- Invalid requests return structured error responses
- Database and external service errors are caught and logged
- HTTP status codes follow REST conventions

# API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These tools were used extensively during frontend integration and testing.

# Testing Strategy

- Pytest is used for automated testing
- A separate test database is configured via environment variables
- Tests cover:
   - Core API routes
   - Database interactions
   - Error handling paths
- Tests can be run locally without affecting development data.

# Deployment Notes

- Environment variables must be configured in production
- Debug mode should be disabled
- Database migrations should be run before serving traffic
- Static assets (images) are served via S3, not the API server


# Eterno Soaps API

FastAPI backend for the Eterno Soaps ecommerce application.

## Related repository
- Frontend: https://github.com/esmerarre/front-end-eterno-soaps

## Requirements
- Python 3.10+
- PostgreSQL

## Environment variables
Create a .env file in the project root with the following variables:

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| SQLALCHEMY_DATABASE_URI | Yes | Postgres connection string for dev/prod | postgresql+psycopg2://user:password@localhost:5432/eterno_soaps_api_development |
| SQLALCHEMY_TEST_DATABASE_URI | Yes (tests) | Postgres connection string for tests | postgresql+psycopg2://user:password@localhost:5432/eterno_soaps_api_test |
| STRIPE_SECRET_KEY | Yes (checkout) | Stripe secret key |  |
| FRONTEND_URL | Yes (checkout) | Frontend base URL for Stripe redirects | http://localhost:5173 |
| SENDGRID_API_KEY | Yes (contact form) | SendGrid API key | SG... |
| FROM_EMAIL | Yes (contact form) | Verified sender email | hello@example.com  *can be identical to TO_EMAIL|
| TO_EMAIL | Yes (contact form) | Destination email for contact form | owner@example.com |
| AWS_ACCESS_KEY_ID | Yes (S3 images) | AWS access key |  |
| AWS_SECRET_ACCESS_KEY | Yes (S3 images) | AWS secret key |  |
| AWS_REGION | Yes (S3 images) | AWS region | us-west-2 |
| AWS_BUCKET_NAME | Yes (S3 images) | S3 bucket name for product images | eterno-soaps-assets |

## AWS S3 Bucket Setup
This application uses AWS S3 to store and serve product images. To set up your S3 bucket:

1. **Create an S3 bucket** in your AWS console with a unique name (e.g., `eterno-soaps-assets`)
 
2. **Create IAM user credentials**:
   - Create an IAM user with programmatic access
   - Attach a policy with `s3:PutObject`, `s3:GetObject`, and `s3:DeleteObject` permissions for your bucket
   - Save the Access Key ID and Secret Access Key to your `.env` file
3. **Set the bucket region** in your `.env` file to match your S3 bucket's region

## Setup
1) Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

2) Install dependencies:
```
pip install -r requirements.txt
```

3) Create Postgres databases:
```
eterno_soaps_api_development
eterno_soaps_api_test
```

4) Run migrations:
```
alembic upgrade head 
```

5) If new models are created or current models are updated. Run migrations:
```
alembic revision --autogenerate -m "added new script for xxx"
alembic upgrade head
```

## Optional: seed data
```
python seed.py
```

Optional image key seeding (requires S3 env vars):
```
python seed_images.py
```

## Run the API
```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000 with docs at http://localhost:8000/docs

## Run tests
```
pytest
```

# Summary

The Eterno Soaps API provides a secure, scalable backend for an ecommerce application, supporting product management, checkout, email communication, and image hosting. It is designed to integrate cleanly with a React frontend and follows best practices for API design, security, and maintainability.