from django.db import models

from users.models import BaseModel, CustomUser


class UserRequisites(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Реквизит пользователя'
        verbose_name_plural = 'Реквизиты пользователя'

    def __str__(self):
        return f'{self.user.username} - {self.bank_name}'

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='requisites',
                             verbose_name='Пользователь')
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    bic = models.CharField(max_length=150, verbose_name='Банковский идентификационный код')
    bank_account = models.CharField(max_length=150, verbose_name='Корреспондентский счет банка')
    user_account = models.CharField(max_length=150, verbose_name='Счет пользователя в банке')
    card_number = models.CharField(max_length=150, verbose_name='Номер карты')
