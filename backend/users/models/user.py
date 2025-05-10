from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    middle_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отчество')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Электронный адрес',
                              error_messages={'unique': 'Пользователь с такой электронной почтой уже существует'})
    phone_number = models.CharField(max_length=150, null=True, blank=True, verbose_name='Номер телефона')
    is_email_verified = models.BooleanField(default=False, verbose_name='Подтверждена почта')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
