from django.db import models

from users.models import BaseModel, CustomUser
from django_prometheus.models import ExportModelOperationsMixin


class UserTemplate(ExportModelOperationsMixin('user_template'), BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = "Шаблон пользователя"
        verbose_name_plural = "Шаблоны пользователя"

    class TemplateTypeChoices(models.TextChoices):
        AGREEMENT = 'AGREEMENT', 'Договор'
        ADDITIONAL = 'ADDITIONAL', 'Дополнение к договору'
        ACT = 'ACT', 'Акт'
        CHECK = 'CHECK', "Чек"
        INVOICES = 'INVOICES', 'Счет'

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='templates',
                             verbose_name='Пользователь')
    title = models.CharField(max_length=150, verbose_name='Название шаблона')
    template_type = models.CharField(max_length=20, choices=TemplateTypeChoices.choices, verbose_name='Тип шаблона')
    content = models.TextField(verbose_name='Тело шаблона')
