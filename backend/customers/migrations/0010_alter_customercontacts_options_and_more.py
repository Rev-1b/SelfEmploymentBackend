# Generated by Django 5.0.6 on 2024-06-25 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customercontacts_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customercontacts',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Контакт заказчика', 'verbose_name_plural': 'Контакты заказчика'},
        ),
        migrations.AlterModelOptions(
            name='customerrequisites',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Реквизит заказчика', 'verbose_name_plural': 'Реквизиты заказчика'},
        ),
    ]