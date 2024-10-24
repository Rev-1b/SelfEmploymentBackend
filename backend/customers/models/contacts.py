from django.db import models

from customers.models import Customer
from users.models import BaseModel


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

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE,
                                 related_name='contacts', verbose_name='Контакты заказчика')
    contact_name = models.CharField(max_length=150, null=True,
                                    verbose_name='Имя контактного лица (может быть не сам заказчик)')
    contact_type = models.CharField(max_length=2, choices=ContactTypes, verbose_name='Тип контакта')
    contact_info = models.CharField(max_length=255, verbose_name='Данные контакта')
