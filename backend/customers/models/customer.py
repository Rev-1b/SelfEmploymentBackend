from django.db import models

from users.models import BaseModel, CustomUser


class Customer(BaseModel):
    class Meta(BaseModel.Meta):
        ordering = ['additional_id']
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.customer_name

    class CustomerTypes(models.TextChoices):
        COMMON = 'CM', 'Физическое лицо'
        LLC = 'LC', 'ООО'
        IE = 'IE', 'Индивидуальный предприниматель'

    additional_id = models.IntegerField(verbose_name='Персональный идентификатор пользователя')
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customers',
                             verbose_name='Пользователь')
    customer_name = models.CharField(max_length=150, verbose_name='ФИО/Сокращенное название')
    customer_type = models.CharField(max_length=2, choices=CustomerTypes)

    # Same fields for LLC and IE
    post_address = models.CharField(max_length=150, verbose_name='Почтовый адрес', null=True, blank=True)
    inn = models.CharField(verbose_name='Идентификационный номер налогоплательщика', null=True, blank=True)

    # LLC Fields
    full_company_name = models.CharField(max_length=150, verbose_name='Полное название компании', null=True, blank=True)
    orgn = models.CharField(max_length=150, verbose_name='Основной гос. регистрационный номер', null=True, blank=True)
    kpp = models.CharField(max_length=150, null=True, blank=True, verbose_name='Код причины постановки на учет')
    legal_address = models.CharField(max_length=255, verbose_name='Юридический адрес', null=True, blank=True)
    okpo = models.CharField(max_length=255, verbose_name='Общероссийский классификатор предприятий и организаций',
                            null=True, blank=True)
    okved = models.CharField(max_length=255,
                             verbose_name='Общероссийский классификатор видов экономической деятельности',
                             null=True, blank=True)

    # IE Fields
    place_of_residence = models.CharField(max_length=150, verbose_name='Адрес прописки', null=True, blank=True)
    ogrnip = models.CharField(
        verbose_name='Основной государственный регистрационный номер индивидуального предпринимателя', null=True,
        blank=True)

    search_fields = ['customer_name']
