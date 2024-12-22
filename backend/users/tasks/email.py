import os

import requests
from users.cryptography import encrypt_data
from celery import shared_task

AUTH_TOKEN = os.getenv('MAILPOST_AUTH_TOKEN')


@shared_task()
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

    # todo: Uncomment in prod
    # response = requests.post(post_url, json=message_params, headers=headers)
    # print(response.status_code)
    # print(response.json())


@shared_task()
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
    # todo: Uncomment in prod
    # response = requests.post(post_url, json=message_params, headers=headers)
    # print(response.status_code)
    # print(response.json())


__all__ = ['send_activation_email', 'send_password_reset_email']