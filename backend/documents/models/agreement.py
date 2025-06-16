from django.db import models

from customers.models import Customer
from users.models import BaseModel

from django_prometheus.models import ExportModelOperationsMixin


class AgreementQuerySet(models.QuerySet):
    def with_sums(self):
        return self.annotate(
            additional_sum=models.Count('additional', distinct=True),
            act_sum=models.Count('acts', distinct=True),
            check_sum=models.Count('checks', distinct=True),
            invoice_sum=models.Count('invoices', distinct=True),
        )


class AgreementManager(models.Manager):
    def get_queryset(self):
        return AgreementQuerySet(self.model, using=self._db)

    def with_sums(self):
        return self.get_queryset().with_sums()


class Agreement(ExportModelOperationsMixin('agreement'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'Договор №{self.number} с заказчиком {self.customer.customer_name}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CREATED', 'Создан'
        SIGNED = 'SIGNED', 'Подписан'
        CLOSED = 'CLOSED', 'Закрыт'
        DISSOLVED = 'DISSOLVED', 'Расторгнут'
        EXPIRED = 'EXPIRED', 'Истек'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='agreements',
                                 verbose_name='Заказчик')
    number = models.CharField(max_length=150, verbose_name='Номер договора')
    content = models.TextField(verbose_name='Текст договора')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус договора')
    deal_amount = models.IntegerField(default=0, verbose_name='Сумма сделки')
    start_date = models.DateField(verbose_name='Дата заключения договора', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания договора', null=True, blank=True)

    objects = AgreementManager()

    search_fields = ['customer__customer_name', 'number']
