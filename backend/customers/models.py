from django.db import models

from users.models import CustomUser, BaseModel, Passport


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

class CustomerPassport(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Паспорт заказчика'
        verbose_name_plural = 'Паспорта заказчиков'
        # unique_together = ['series', 'number']

    def __str__(self):
        return f'{self.series}{self.number}'

    customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, related_name='passport',
                                    null=True, blank=True, verbose_name='Заказчик')
    series = models.CharField(max_length=150, verbose_name='Серия паспорта')
    number = models.CharField(max_length=150, verbose_name='Номер паспорта')
    release_date = models.DateField(max_length=150, verbose_name='Дата выдачи')
    issued = models.CharField(max_length=150, verbose_name='Выдан')
    unit_code = models.CharField(max_length=7, verbose_name='Код подразделения')


class CustomerRequisites(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Реквизит заказчика'
        verbose_name_plural = 'Реквизиты заказчика'

    def __str__(self):
        return f'{self.customer.customer_name} - {self.bank_name}'

    customer = models.ForeignKey(to='Customer', on_delete=models.CASCADE, related_name='requisites')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.CharField(max_length=150, verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    customer_account_number = models.CharField(max_length=150, verbose_name='Номер расчетного счета заказчика')


class CustomerContacts(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Контакт заказчика'
        verbose_name_plural = 'Контакты заказчика'

    def __str__(self):
        return f'{self.contact_name} - {self.contact_type}'

    class ContactTypes(models.TextChoices):
        PHONE = 'PH', 'Телефон'
        EMAIL = 'EL', 'Электронная почта'
        TELEGRAM = 'TG', 'Аккаунт Телеграм'
        WHATSAPP = 'WA', "Аккаунт What's App"
        CUSTOMERSITE = 'CS', 'Сайт заказчика'

    customer = models.ForeignKey(to='Customer', on_delete=models.CASCADE,
                                 related_name='contacts', verbose_name='Контакты заказчика')
    contact_name = models.CharField(max_length=150, null=True,
                                    verbose_name='Имя контактного лица (может быть не сам заказчик)')
    contact_type = models.CharField(max_length=2, choices=ContactTypes, verbose_name='Тип контакта')
    contact_info = models.CharField(max_length=255, verbose_name='Данные контакта')
