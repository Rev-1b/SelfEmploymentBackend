from django.db import models

from users.models import CustomUser


class Customer(models.Model):
    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.customer_name

    class CustomerTypes(models.TextChoices):
        COMMON = 'CM', 'Физическое лицо'
        LLC = 'LC', 'ООО'
        IE = 'IE', 'Индивидуальный предприниматель'

    additional_id = models.IntegerField(unique=True, verbose_name='Персональный идентификатор пользователя')
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customers',
                             verbose_name='Заказчики')
    customer_name = models.CharField(max_length=150, verbose_name='ФИО/Сокращенное название')
    customer_type = models.CharField(max_length=2, choices=CustomerTypes)

    # Common fields for LLC and IE
    post_address = models.CharField(max_length=150, verbose_name='Почтовый адрес')
    inn = models.IntegerField(verbose_name='Идентификационный номер налогоплательщика')

    # LLC Fields
    full_company_name = models.CharField(max_length=150, verbose_name='Полное название компании')
    orgn = models.IntegerField(verbose_name='Основной гос. регистрационный номер')
    kpp = models.IntegerField(blank=True, null=True, verbose_name='Код причины постановки на учет')
    legal_address = models.CharField(max_length=255, verbose_name='Юридический адрес')
    okpo = models.CharField(max_length=255, verbose_name='Общероссийский классификатор предприятий и организаций')
    okved = models.CharField(max_length=255,
                             verbose_name='Общероссийский классификатор видов экономической деятельности')

    # IE Fields
    place_of_residence = models.CharField(max_length=150, verbose_name='Адрес прописки')
    ogrnip = models.CharField(
        verbose_name='Основной государственный регистрационный номер индивидуального предпринимателя')


# class LLCCustomer(models.Model):
#     customer = models.OneToOneField(to='Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='LLC',
#                                     verbose_name='Заказчик')
#     full_company_name = models.CharField(max_length=150, verbose_name='Полное название компании')
#     orgn = models.IntegerField(verbose_name='Основной гос. регистрационный номер')
#     inn = models.IntegerField(verbose_name='Идентификационный номер налогоплательщика')
#     kpp = models.IntegerField(blank=True, null=True, verbose_name='Код причины постановки на учет')
#     legal_address = models.CharField(max_length=255, verbose_name='Юридический адрес')
#     post_address = models.CharField(max_length=255, verbose_name='Почтовый адрес')
#     okpo = models.CharField(max_length=255, verbose_name='Общероссийский классификатор предприятий и организаций')
#     okved = models.CharField(max_length=255,
#                              verbose_name='Общероссийский классификатор видов экономической деятельности')
#
#
# class IECustomer(models.Model):
#     customer = models.OneToOneField(to='Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='IE',
#                                     verbose_name='Заказчик')
#     place_of_residence = models.CharField(max_length=150, verbose_name='Адрес прописки')
#     post_address = models.CharField(max_length=150, verbose_name='Почтовый адрес')
#     inn = models.IntegerField(verbose_name='Идентификационный номер налогоплательщика')
#     ogrnip = models.CharField(
#         verbose_name='Основной государственный регистрационный номер индивидуального предпринимателя')


class CustomerRequisites(models.Model):
    class Meta:
        verbose_name = 'Реквизит пользователя'
        verbose_name_plural = 'Реквизиты пользователя'

    def __str__(self):
        return f'{self.customer.name} - {self.bank_name}'

    customer = models.ForeignKey(to='Customer', on_delete=models.CASCADE, related_name='requisites')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.IntegerField(verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    customer_account_number = models.IntegerField(verbose_name='Номер расчетного счета заказчика')


# class CustomerContacts(models.Model):
#     customer = models.OneToOneField(to='Customer', on_delete=models.CASCADE, related_name='all_contacts',
#                                     verbose_name='Заказчик')
#     contact_name = models.CharField(max_length=150, null=True, blank=True,
#                                     verbose_name='Имя контактного лица (может быть не сам заказчик)')


class CustomerContacts(models.Model):
    class Meta:
        verbose_name = 'Контакт пользователя'
        verbose_name_plural = 'Контакты пользователя'

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
    contact_name = models.CharField(max_length=150, null=True, blank=True,
                                    verbose_name='Имя контактного лица (может быть не сам заказчик)')
    contact_type = models.CharField(max_length=2, choices=ContactTypes, verbose_name='Тип контакта')
    contact_info = models.CharField(max_length=255, verbose_name='Данные контакта')
