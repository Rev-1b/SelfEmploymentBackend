# Generated by Django 5.0.6 on 2024-06-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_alter_act_options_alter_additional_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='act',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Акт', 'verbose_name_plural': 'Акты'},
        ),
        migrations.AlterModelOptions(
            name='additional',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Дополнение к договору', 'verbose_name_plural': 'Дополнения к договору'},
        ),
        migrations.AlterModelOptions(
            name='agreement',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Договор', 'verbose_name_plural': 'Договоры'},
        ),
        migrations.AlterModelOptions(
            name='checkmodel',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Чек', 'verbose_name_plural': 'Чеки'},
        ),
        migrations.AlterModelOptions(
            name='deal',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Сделка', 'verbose_name_plural': 'Сделки'},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Счет', 'verbose_name_plural': 'Счета'},
        ),
        migrations.AlterModelOptions(
            name='usertemplate',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Шаблон пользователя', 'verbose_name_plural': 'Шаблоны пользователя'},
        ),
    ]
