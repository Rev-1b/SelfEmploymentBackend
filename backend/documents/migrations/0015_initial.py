# Generated by Django 5.0.6 on 2024-06-25 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0010_alter_customercontacts_options_and_more'),
        ('documents', '0014_remove_act_additional_remove_act_agreement_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agreement_number', models.CharField(max_length=16, verbose_name='Номер договора')),
                ('content', models.TextField(verbose_name='Текст договора')),
                ('status', models.CharField(choices=[('CR', 'Создан'), ('SG', 'Подписан'), ('CL', 'Закрыт'), ('DS', 'Расторгнут'), ('EX', 'Истек')], default='CR', max_length=2, verbose_name='Статус договора')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='customers.customer', verbose_name='Договоры')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договоры',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, verbose_name='Название дополнения')),
                ('content', models.TextField(verbose_name='Текст дополнения')),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional', to='documents.agreement', verbose_name='Дополнения к договору')),
            ],
            options={
                'verbose_name': 'Дополнение к договору',
                'verbose_name_plural': 'Дополнения к договору',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, verbose_name='Название акта')),
                ('content', models.TextField(verbose_name='Текст акта')),
                ('status', models.CharField(choices=[('CR', 'Создан'), ('CL', 'Закрыт')], default='CR', max_length=2, verbose_name='Статус акта')),
                ('additional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acts', to='documents.additional')),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acts', to='documents.agreement')),
            ],
            options={
                'verbose_name': 'Акт',
                'verbose_name_plural': 'Акты',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(verbose_name='Сумма чека')),
                ('additional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='documents.additional')),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='documents.agreement')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service_type', models.CharField(max_length=150, verbose_name='Вид сделки')),
                ('amount', models.IntegerField(verbose_name='Сумма сделки')),
                ('service_date', models.DateField(verbose_name='Дата заключения сделки')),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='documents.agreement', verbose_name='Договор')),
            ],
            options={
                'verbose_name': 'Сделка',
                'verbose_name_plural': 'Сделки',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(verbose_name='Сумма счета')),
                ('status', models.CharField(choices=[('CR', 'Создан'), ('CL', 'Закрыт')], default='CR', max_length=2, verbose_name='Статус счета')),
                ('additional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='documents.additional')),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='documents.agreement')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, verbose_name='Название шаблона')),
                ('template_type', models.CharField(choices=[('AG', 'Договор'), ('AD', 'Дополнение к договору'), ('AC', 'Акт'), ('CH', 'Чек'), ('IN', 'Счет')], max_length=2, verbose_name='Тип шаблона')),
                ('content', models.TextField(verbose_name='Тело шаблона')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Шаблон пользователя',
                'verbose_name_plural': 'Шаблоны пользователя',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
    ]
