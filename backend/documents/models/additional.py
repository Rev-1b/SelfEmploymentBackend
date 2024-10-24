from django.db import models

from documents.models.agreement import Agreement
from users.models import BaseModel


class AdditionalQuerySet(models.QuerySet):
    def with_sums(self):
        return self.annotate(
            act_sum=models.Count('acts', distinct=True),
            check_sum=models.Count('checks', distinct=True),
            invoice_sum=models.Count('invoices', distinct=True),
        )


class AdditionalManager(models.Manager):
    def get_queryset(self):
        return AdditionalQuerySet(self.model, using=self._db)

    def with_sums(self):
        return self.get_queryset().with_sums()


class Additional(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Дополнение к договору'
        verbose_name_plural = 'Дополнения к договору'

    class StatusChoices(models.TextChoices):
        CREATED = 'CR', 'Создан'
        CLOSED = 'CL', 'Закрыт'

    def __str__(self):
        return f'Дополнение {self.title} к договору {self.agreement}'

    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, related_name='additional',
                                  verbose_name='Дополнения к договору')
    number = models.CharField(max_length=160, verbose_name='Номер Дополнения')
    title = models.CharField(max_length=150, verbose_name='Название дополнения')
    content = models.TextField(verbose_name='Текст дополнения')
    deal_amount = models.IntegerField(default=0, verbose_name='Сумма сделки')
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус Дополнения')

    objects = AdditionalManager()

    search_fields = ['agreement__customer__customer_name', 'number', 'title']
