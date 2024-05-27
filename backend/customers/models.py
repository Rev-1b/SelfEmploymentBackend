from django.db import models

from users.models import CustomUser


class Customer(models.Model):
    additional_id = models.IntegerField(unique=True, verbose_name='Персональный идентификатор пользователя')
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customers',
                             verbose_name='Заказчики')
    customer_name = models.CharField(max_length=150, verbose_name='ФИО/Сокращенное название')


class LLCCustomer(models.Model):
    customer = models.OneToOneField(to='Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='LLC',
                                    verbose_name='Заказчик')
    full_company_name = models.CharField(max_length=150, verbose_name='Полное название компании')
    orgn = models.IntegerField(verbose_name='Основной гос. регистрационный номер')
    inn = models.IntegerField(verbose_name='Идентификационный номер налогоплательщика')
    kpp = models.IntegerField(blank=True, null=True, verbose_name='Код причины постановки на учет')
    legal_address = models.CharField(max_length=255, verbose_name='Юридический адрес')
    post_address = models.CharField(max_length=255, verbose_name='Почтовый адрес')
    okpo = models.CharField(max_length=255, verbose_name='Общероссийский классификатор предприятий и организаций')
    okved = models.CharField(max_length=255,
                             verbose_name='Общероссийский классификатор видов экономической деятельности')


class IECustomer(models.Model):
    customer = models.OneToOneField(to='Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='IE',
                                    verbose_name='Заказчик')
    place_of_residence = models.CharField(max_length=150, verbose_name='Адрес прописки')
    post_address = models.CharField(max_length=150, verbose_name='Почтовый адрес')
    inn = models.IntegerField(verbose_name='Идентификационный номер налогоплательщика')
    ogrnip = models.CharField(
        verbose_name='Основной государственный регистрационный номер индивидуального предпринимателя')
