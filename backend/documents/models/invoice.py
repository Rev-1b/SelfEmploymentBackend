from django.db import models

from documents.models.additional import Additional
from documents.models.agreement import Agreement
from users.models import BaseModel


class Invoice(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'Счет на {self.amount} к договору {self.agreement}' if self.agreement else \
            f'Счет на {self.amount} к дополнению {self.additional}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CREATED', 'Создан'
        CLOSED = 'CLOSED', 'Закрыт'

    number = models.CharField(max_length=160, verbose_name='Номер Счета')
    amount = models.IntegerField(verbose_name='Сумма счета')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='invoices')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='invoices')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус счета')

    search_fields = ['agreement__customer__customer_name', 'additional__agreement__customer__customer_name', 'number']
