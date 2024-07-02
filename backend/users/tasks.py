from django.contrib.auth.tokens import default_token_generator
from .cryptography import encrypt_data, decrypt_data


def send_activation_email(base_url, user):
    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    user_id_new = decrypt_data(confirmation_token)

    "Здесь посылаем запрос на почтовый сервер"


def send_password_reset_email(base_url, user):
    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    user_id_new = decrypt_data(confirmation_token)

    "Здесь посылаем запрос на почтовый сервер"