from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Электронный адрес', max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Passport(models.Model):
    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'

    def __str__(self):
        return f'{self.series}{self.number}'

    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='passport',
                                verbose_name='Пользователь')
    series = models.IntegerField(verbose_name='Серия паспорта')
    number = models.IntegerField(verbose_name='Номер паспорта')
    release_date = models.DateField(verbose_name='Дата выдачи')
    unit_code = models.CharField(max_length=7, verbose_name='Код подразделения')


class AdvertiseInfo(models.Model):
    class Meta:
        verbose_name = 'Пакет рекламной информации'
        verbose_name_plural = 'Пакеты рекламной информации'

    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='advertise_info',
                                verbose_name='Пользователь')
    utm_source = models.CharField()
    utm_content = models.CharField()
    utm_medium = models.CharField()
    utm_term = models.CharField()
    utm_campaign = models.CharField()


class UserRequisites(models.Model):
    class Meta:
        verbose_name = 'Реквизит пользователя'
        verbose_name_plural = 'Реквизиты пользователя'

    def __str__(self):
        return f'{self.user.username} - {self.bank_name}'

    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, related_name='requisites',
                             verbose_name='Пользователь')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.IntegerField(verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    user_account = models.CharField(max_length=150, verbose_name='Счет пользователя в банке')
    card_number = models.IntegerField(verbose_name='Номер карты')
