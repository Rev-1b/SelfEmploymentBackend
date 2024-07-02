from itsdangerous import URLSafeSerializer
from django.conf import settings


def encrypt_data(data):
    serializer = URLSafeSerializer(secret_key=settings.SECRET_KEY)
    token = serializer.dumps(data)
    return token


def decrypt_data(token):
    serializer = URLSafeSerializer(secret_key=settings.SECRET_KEY)
    try:
        data = serializer.loads(token)
        return data
    except Exception as e:
        return None