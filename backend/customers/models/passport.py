from django.db import models

from customers.models.customer import Customer
from users.models import BaseModel

from django_prometheus.models import ExportModelOperationsMixin


class CustomerPassport(ExportModelOperationsMixin('customer_passport'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Паспорт заказчика'
        verbose_name_plural = 'Паспорта заказчиков'
        # unique_together = ['series', 'number']

    def __str__(self):
        return f'{self.series}{self.number}'

    customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, related_name='passport',
                                    null=True, blank=True, verbose_name='Заказчик')
    series = models.CharField(max_length=150, verbose_name='Серия паспорта')
    number = models.CharField(max_length=150, verbose_name='Номер паспорта')
    release_date = models.DateField(max_length=150, verbose_name='Дата выдачи')
    issued = models.CharField(max_length=150, verbose_name='Выдан')
    unit_code = models.CharField(max_length=7, verbose_name='Код подразделения')
