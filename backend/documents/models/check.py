from django.db import models

from documents.models.additional import Additional
from documents.models.agreement import Agreement
from users.models import BaseModel

from django_prometheus.models import ExportModelOperationsMixin


class CheckModel(ExportModelOperationsMixin('check'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f'Чек на {self.amount} к договору {self.agreement}' if self.agreement else \
            f'Чек на {self.amount} к дополнению {self.additional}'

    number = models.CharField(max_length=160, verbose_name='Номер Чека')
    amount = models.IntegerField(verbose_name='Сумма чека')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True, related_name='checks')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='checks')

    search_fields = ['agreement__customer__customer_name', 'additional__agreement__customer__customer_name', 'number']
