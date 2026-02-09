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