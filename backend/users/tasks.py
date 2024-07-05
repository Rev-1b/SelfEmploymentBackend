import requests

from .cryptography import encrypt_data, decrypt_data


def send_activation_email(base_url, user):
    AUTH_TOKEN = 'a663bb11a4377ce5bd5aa775577c7a5f'
    post_url = 'https://api.mailopost.ru/v1/email/messages/'

    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    message_params = {
        "from_email": "new.luenkoaleksei@gmail.com",
        "from_name": "Рога и Копыта",
        "to": "ugsearmany@gmail.com",
        "subject": 'Активация электронной почты на сайте "Рога и копыта"',
        "html": f'<h1>Здравствуйте, дорогой пользователь!</h1>'
                f'<div>Для подтверждения своей почты просим вас перейти по ссылке:<a href="{activation_link}"></div>',
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(post_url, json=message_params, headers=headers)
    print(response.status_code)
    print(response.json())


def send_password_reset_email(base_url, user):
    confirmation_token = encrypt_data(user.pk)
    activation_link = f'{base_url}?confirmation_token={confirmation_token}'

    user_id_new = decrypt_data(confirmation_token)

    "Здесь посылаем запрос на почтовый сервер"
