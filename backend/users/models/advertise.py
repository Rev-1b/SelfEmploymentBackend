from django.db import models

from users.models import BaseModel
from users.models import CustomUser


class AdvertiseInfo(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = 'Пакет рекламной информации'
        verbose_name_plural = 'Пакеты рекламной информации'

    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='advertise_info',
                                verbose_name='Пользователь')
    utm_source = models.CharField()
    utm_content = models.CharField()
    utm_medium = models.CharField()
    utm_term = models.CharField()
    utm_campaign = models.CharField()
    partner_id = models.IntegerField()
