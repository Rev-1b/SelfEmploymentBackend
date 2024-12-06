import os
from datetime import timedelta

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://*.176.123.169.4', 'https://*.176.123.169.4']

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
    'http://127.0.0.1:5175',
    'http://127.0.0.1:5176',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),  # Изменено на JWT вместо Bearer
}


# CELERY_RESULT_BACKEND = 'django-db'
BROKER_USER = os.getenv('RABBITMQ_DEFAULT_USER')
BROKER_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = int(os.getenv('BROKER_PORT', '5672'))

CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASS}@{BROKER_HOST}:{BROKER_PORT}/"