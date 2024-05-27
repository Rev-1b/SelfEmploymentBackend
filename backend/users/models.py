from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')
    passport = models.OneToOneField(to='Passport', on_delete=models.CASCADE, related_name='user')
    advertise_info = models.OneToOneField(to='AdvertiseInfo', on_delete=models.CASCADE, related_name='user')


class Passport(models.Model):
    series = models.IntegerField(verbose_name='Серия паспорта')
    number = models.IntegerField(verbose_name='Номер паспорта')
    release_date = models.DateField(verbose_name='Дата выдачи')
    unit_code = models.CharField(max_length=7, verbose_name='Код подразделения')


class AdvertiseInfo(models.Model):
    utm_source = models.CharField()
    utm_content = models.CharField()
    utm_medium = models.CharField()
    utm_term = models.CharField()
    utm_campaign = models.CharField()


class UserRequisites(models.Model):
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, related_name='requisites')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.IntegerField(verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    user_account = models.CharField(max_length=150, verbose_name='Счет пользователя в банке')
    card_number = models.IntegerField(verbose_name='Номер карты')
