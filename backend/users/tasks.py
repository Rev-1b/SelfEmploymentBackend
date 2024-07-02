from django.contrib.auth.tokens import default_token_generator


def send_activation_email(base_url, user):
    confirmation_token = default_token_generator.make_token(user)
    activation_link = f'{base_url}?user_id={user.id}&confirmation_token={confirmation_token}'

    "Здесь посылаем запрос на почтовый сервер"


def send_password_reset_email(base_url)