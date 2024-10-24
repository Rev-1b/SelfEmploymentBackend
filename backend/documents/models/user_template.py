from django.db import models

from users.models import BaseModel, CustomUser


class UserTemplate(BaseModel):
    class Meta(BaseModel.Meta):
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
    template_type = models.CharField(max_length=2, choices=TemplateTypeChoices.choices, verbose_name='Тип шаблона')
    content = models.TextField(verbose_name='Тело шаблона')
