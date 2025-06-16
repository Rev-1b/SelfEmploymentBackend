from django.db import models

from customers.models import Customer
from users.models import BaseModel

from django_prometheus.models import ExportModelOperationsMixin


class CustomerContacts(ExportModelOperationsMixin("customer_contacts"), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Контакт заказчика'
        verbose_name_plural = 'Контакты заказчика'

    def __str__(self):
        return f'{self.contact_name} - {self.contact_type}'

    class ContactTypes(models.TextChoices):
        PHONE = 'PHONE', 'Телефон'
        EMAIL = 'EMAIL', 'Электронная почта'
        TELEGRAM = 'TELEGRAM', 'Аккаунт Телеграм'
        WHATSAPP = 'WHATSAPP', "Аккаунт What's App"
        CUSTOMERSITE = 'CUSTOMERSITE', 'Сайт заказчика'

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                 related_name='contacts', verbose_name='Контакты заказчика')
    contact_name = models.CharField(max_length=150, null=True,
                                    verbose_name='Имя контактного лица (может быть не сам заказчик)')
    contact_type = models.CharField(max_length=20, choices=ContactTypes, verbose_name='Тип контакта')
    contact_info = models.CharField(max_length=255, verbose_name='Данные контакта')
