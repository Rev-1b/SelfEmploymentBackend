# Generated by Django 5.0.6 on 2024-06-10 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_full_company_name_alter_customer_inn_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customercontacts',
            options={'verbose_name': 'Контакт заказчика', 'verbose_name_plural': 'Контакты заказчика'},
        ),
    ]
