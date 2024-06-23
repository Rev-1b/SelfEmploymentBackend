from django.db import models

from customers.models import Customer, CustomUser
from users.models import CustomModel


class Agreement(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'Договор №{self.agreement_number} с заказчиком {self.customer.customer_name}'

    class StatusChoices(models.TextChoices):
        CREATED = 'CR', 'Создан'
        SIGNED = 'SG', 'Подписан'
        CLOSED = 'CL', 'Закрыт'
        DISSOLVED = 'DS', 'Расторгнут'
        EXPIRED = 'EX', 'Истек'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='agreements',
                                 verbose_name='Договоры')
    agreement_number = models.CharField(max_length=16, verbose_name='Номер договора')
    content = models.TextField(verbose_name='Текст договора')
    status = models.CharField(max_length=2, choices=StatusChoices.choices, default=StatusChoices.CREATED,
                              verbose_name='Статус договора')


class Additional(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = 'Дополнение к договору'
        verbose_name_plural = 'Дополнения к договору'

    def __str__(self):
        return f'Дополнение {self.title} к договору {self.agreement}'

    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, related_name='additional',
                                  verbose_name='Дополнения к договору')
    title = models.CharField(max_length=150, verbose_name='Название дополнения')
    content = models.TextField(verbose_name='Текст дополнения')


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


class Deal(CustomModel):
    class Meta(CustomModel.Meta):
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, related_name='deals',
                                  verbose_name='Договор')
    service_type = models.CharField(max_length=150, verbose_name='Вид сделки')
    amount = models.IntegerField(verbose_name='Сумма сделки')
    service_date = models.DateField(verbose_name='Дата заключения сделки')
