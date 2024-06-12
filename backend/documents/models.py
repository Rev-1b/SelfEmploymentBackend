from django.db import models

from customers.models import Customer


class Agreement(models.Model):
    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'Договор №{self.agreement_number} с заказчиком {self.customer.customer_name}'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='agreements',
                                 verbose_name='Договоры')
    agreement_number = models.CharField(max_length=16, verbose_name='Номер договора')
    content = models.TextField(verbose_name='Текст договора')


class Additional(models.Model):
    class Meta:
        verbose_name = 'Дополнение к договору'
        verbose_name_plural = 'Дополнения к договору'

    def __str__(self):
        return f'Дополнение {self.title} к договору {self.agreement}'

    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, related_name='additional',
                                  verbose_name='Дополнения к договору')
    title = models.CharField(max_length=150, verbose_name='Название дополнения')
    content = models.TextField(verbose_name='Текст дополнения')


class Act(models.Model):
    class Meta:
        verbose_name = 'Акт'
        verbose_name_plural = 'Акты'

    def __str__(self):
        return f'Акт {self.title} к договору {self.agreement}' if self.agreement else \
            f'Акт {self.title} к дополнению {self.additional}'

    title = models.CharField(max_length=150, verbose_name='Название акта')
    content = models.TextField(verbose_name='Текст акта')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True, related_name='acts')
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True, related_name='acts')


class Invoice(models.Model):
    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'Счет на {self.amount} к договору {self.agreement}' if self.agreement else \
            f'Счет на {self.amount} к дополнению {self.additional}'

    amount = models.IntegerField(verbose_name='Сумма счета')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True)
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True)


class CheckModel(models.Model):
    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f'Чек на {self.amount} к договору {self.agreement}' if self.agreement else \
            f'Чек на {self.amount} к дополнению {self.additional}'

    amount = models.IntegerField(verbose_name='Сумма чека')
    agreement = models.ForeignKey(to=Agreement, on_delete=models.CASCADE, null=True, blank=True)
    additional = models.ForeignKey(to=Additional, on_delete=models.CASCADE, null=True, blank=True)
