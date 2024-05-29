from django.db import models


class Agreement(models.Model):
    customer = models.ForeignKey(to='Customer', on_delete=models.CASCADE, related_name='agreements',
                                 verbose_name='Договоры')
    agreement_number = models.CharField(max_length=16, verbose_name='Номер договора')
    content = models.TextField(verbose_name='Текст договора')


class Additional(models.Model):
    agreement = models.ForeignKey(to='Agreement', on_delete=models.CASCADE, related_name='additional',
                                  verbose_name='Дополнения к договору')
    title = models.CharField(max_length=150, verbose_name='Название дополнения')
    content = models.TextField(verbose_name='Текст дополнения')


class BaseAttachment(models.Model):
    agreement = models.ForeignKey(to='Agreement', on_delete=models.CASCADE, related_name='base_attachment',
                                  blank=True, null=True)
    additional = models.ForeignKey(to='Additional', on_delete=models.CASCADE, related_name='base_attachment',
                                   blank=True, null=True)


class Act(BaseAttachment):
    title = models.CharField(max_length=150, verbose_name='Название акта')
    content = models.TextField(verbose_name='Текст акта')


class Check(BaseAttachment):
    amount = models.IntegerField(verbose_name='Сумма')
