from django.db import models

from users.models import BaseModel
from users.models import CustomUser

from django_prometheus.models import ExportModelOperationsMixin


class Passport(ExportModelOperationsMixin('user_passport'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Паспорт пользователя'
        verbose_name_plural = 'Паспорта пользователей'
        # unique_together = ['series', 'number']

    def __str__(self):
        return f'{self.series}{self.number}'

    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='passport',
                                verbose_name='Пользователь')
    series = models.CharField(max_length=150, verbose_name='Серия паспорта')
    number = models.CharField(max_length=150, verbose_name='Номер паспорта')
    release_date = models.DateField(max_length=150, verbose_name='Дата выдачи')
    issued = models.CharField(max_length=150, verbose_name='Выдан')
    unit_code = models.CharField(max_length=7, verbose_name='Код подразделения')
