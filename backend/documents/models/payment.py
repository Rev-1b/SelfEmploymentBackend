from django.db import models

from documents.models.act import Act
from documents.models.additional import Additional
from documents.models.agreement import Agreement
from documents.models.check import CheckModel
from documents.models.invoice import Invoice
from users.models import BaseModel


class PaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            amount=models.Case(
                models.When(invoice__isnull=True, check_link__isnull=True, then=models.Value(None)),
                models.When(invoice__isnull=False, check_link__isnull=True, then=models.F('invoice__amount')),
                models.When(invoice__isnull=True, check_link__isnull=False, then=models.F('check_link__amount')),
                models.When(invoice__isnull=False, check_link__isnull=False, then=models.F('check_link__amount')),
                output_field=models.DecimalField(max_digits=10, decimal_places=2)
            )
        )

    def with_check(self):
        return self.get_queryset().filter(check_link__isnull=False)

    def without_check(self):
        return self.get_queryset().filter(check_link__isnull=True)


class Payment(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    class StatusChoices(models.TextChoices):
        INITIATED = 'INITIATED', 'Инициирован'
        CLOSED = 'CLOSED', 'Проведен'

    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, related_name='payments',
                                  null=True, blank=True, verbose_name='Договор')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, related_name='payments',
                                   null=True, blank=True, verbose_name='Дополнение')
    act = models.ForeignKey(to=Act, on_delete=models.CASCADE, related_name='payment',
                            null=True, blank=True, verbose_name='Акт')
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, related_name='payment',
                                null=True, blank=True, verbose_name='Счет')
    check_link = models.ForeignKey(to=CheckModel, on_delete=models.CASCADE, related_name='payment',
                                   null=True, blank=True, verbose_name='Чек')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.INITIATED,
                              verbose_name='Статус счета')

    objects = PaymentManager()

    search_fields = ['agreement__customer__customer_name']
