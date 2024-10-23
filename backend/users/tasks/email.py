import requests
from users.cryptography import encrypt_data

AUTH_TOKEN = '4504a59d63fdb8f7c5a6b7a408210cdf'


def send_activation_email(base_url, user):
    post_url = 'https://api.mailopost.ru/v1/email/lists/570409/recipients'

    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    message_params = {
        "email": user.email,
        "values": [
            {
                "parameter_id": "402203",
                "value": activation_link
            },
            {
                "parameter_id": "402182",
                "value": user.username if user.username is not None else ""
            }
        ],
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(post_url, json=message_params, headers=headers)
    print(response.status_code)
    print(response.json())


def send_password_reset_email(base_url, user):
    post_url = 'https://api.mailopost.ru/v1/email/lists/570421/recipients'

    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    message_params = {
        "email": user.email,
        "values": [
            {
                "parameter_id": "402184",
                "value": activation_link
            },
            {
                "parameter_id": "402183",
                "value": user.username if user.username is not None else ""
            }
        ],
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(post_url, json=message_params, headers=headers)
    print(response.status_code)
    print(response.json())


__all__ = ['send_activation_email', 'send_password_reset_email']