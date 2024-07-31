from django.db import models

from customers.models import Customer, CustomUser
from users.models import CustomModel


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


class Agreement(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'Договор №{self.number} с заказчиком {self.customer.customer_name}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CR', 'Создан'
        SIGNED = 'SG', 'Подписан'
        CLOSED = 'CL', 'Закрыт'
        DISSOLVED = 'DS', 'Расторгнут'
        EXPIRED = 'EX', 'Истек'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='agreements',
                                 verbose_name='Договоры')
    number = models.CharField(max_length=150, verbose_name='Номер договора')
    content = models.TextField(verbose_name='Текст договора')
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус договора')
    deal_amount = models.IntegerField(default=0, verbose_name='Сумма сделки')
    start_date = models.DateField(verbose_name='Дата заключения договора', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата окончания договора', null=True, blank=True)

    objects = AgreementManager()


# ----------------------------------------------------------------------------------------------------------------------
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


class Additional(CustomModel):
    class Meta(CustomModel.Meta):
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


class Act(CustomModel):
    class Meta(CustomModel.Meta):
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
    status = models.CharField(max_length=2, choices=StatusChoices, default=StatusChoices.CREATED,
                              verbose_name='Статус акта')


class Invoice(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'Счет на {self.amount} к договору {self.agreement}' if self.agreement else \
            f'Счет на {self.amount} к дополнению {self.additional}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CR', 'Создан'
        CLOSED = 'CL', 'Закрыт'

    number = models.CharField(max_length=160, verbose_name='Номер Счета')
    amount = models.IntegerField(verbose_name='Сумма счета')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='invoices')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='invoices')
    status = models.CharField(max_length=2, choices=StatusChoices, default=StatusChoices.CREATED,
                              verbose_name='Статус счета')


class CheckModel(CustomModel):
    class Meta(CustomModel.Meta):
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


class UserTemplate(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = "Шаблон пользователя"
        verbose_name_plural = "Шаблоны пользователя"

    class TemplateTypeChoices(models.TextChoices):
        AGREEMENT = 'AG', 'Договор'
        ADDITIONAL = 'AD', 'Дополнение к договору'
        ACT = 'AC', 'Акт'
        CHECK = 'CH', "Чек"
        INVOICES = 'IN', 'Счет'

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='templates',
                             verbose_name='Пользователь')
    title = models.CharField(max_length=150, verbose_name='Название шаблона')
    template_type = models.CharField(max_length=2, choices=TemplateTypeChoices, verbose_name='Тип шаблона')
    content = models.TextField(verbose_name='Тело шаблона')


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


class Payment(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

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

    objects = PaymentManager()
