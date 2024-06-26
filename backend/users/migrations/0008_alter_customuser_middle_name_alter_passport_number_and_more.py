# Generated by Django 5.0.6 on 2024-06-07 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_advertiseinfo_partner_id_alter_userrequisites_bic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(default='', max_length=150, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='number',
            field=models.CharField(max_length=150, verbose_name='Номер паспорта'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='release_date',
            field=models.DateField(max_length=150, verbose_name='Дата выдачи'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='series',
            field=models.CharField(max_length=150, verbose_name='Серия паспорта'),
        ),
    ]
