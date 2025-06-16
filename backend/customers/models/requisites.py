from django.db import models

from customers.models import Customer
from users.models import BaseModel

from django_prometheus.models import ExportModelOperationsMixin


class CustomerRequisites(ExportModelOperationsMixin('customer_requisites'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Реквизит заказчика'
        verbose_name_plural = 'Реквизиты заказчика'

    def __str__(self):
        return f'{self.customer.customer_name} - {self.bank_name}'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='requisites')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.CharField(max_length=150, verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    customer_account_number = models.CharField(max_length=150, verbose_name='Номер расчетного счета заказчика')
