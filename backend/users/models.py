from django.db import models
from django.contrib.auth.models import AbstractUser


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
