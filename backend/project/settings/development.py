from datetime import timedelta

DEBUG = True
SECRET_KEY = 'django-insecure-&7f_u76e*=d@1+1j8*rm-e7l04$7#4%ogae7kczfm003257_6i'

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']

CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'employment',
        "USER": 'observer_user',
        "PASSWORD": 'qwerty2F',
        "HOST": 'localhost',
        "PORT": "5432",
    }
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'AUTH_HEADER_TYPES': ('JWT',)
}

# CELERY_RESULT_BACKEND = 'django-db'
BROKER_USER = 'admin'
BROKER_PASS = 'admin'
BROKER_HOST = 'rabbitmq'
BROKER_PORT = 5672

CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASS}@{BROKER_HOST}:{BROKER_PORT}/"