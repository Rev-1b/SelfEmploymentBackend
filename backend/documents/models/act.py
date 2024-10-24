from django.db import models

from documents.models.additional import Additional
from documents.models.agreement import Agreement
from users.models import BaseModel


class Act(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Акт'
        verbose_name_plural = 'Акты'

    def __str__(self):
        return f'Акт {self.title} к договору {self.agreement}' if self.agreement else \
            f'Акт {self.title} к дополнению {self.additional}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CR', 'Создан'
        CLOSED = 'CL', 'Закрыт'

    number = models.CharField(max_length=160, verbose_name='Номер Акта')
    title = models.CharField(max_length=150, verbose_name='Название акта')
    content = models.TextField(verbose_name='Текст акта')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True, related_name='acts')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True, related_name='acts')
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус акта')

    search_fields = ['agreement__customer__customer_name', 'additional__agreement__customer__customer_name', 'number',
                     'title']
