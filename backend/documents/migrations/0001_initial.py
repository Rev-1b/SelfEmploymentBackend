# Generated by Django 5.0.6 on 2024-10-23 13:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, verbose_name='Название шаблона')),
                ('template_type', models.CharField(choices=[('AG', 'Договор'), ('AD', 'Дополнение к договору'), ('AC', 'Акт'), ('CH', 'Чек'), ('IN', 'Счет')], max_length=2, verbose_name='Тип шаблона')),
                ('content', models.TextField(verbose_name='Тело шаблона')),
            ],
            options={
                'verbose_name': 'Шаблон пользователя',
                'verbose_name_plural': 'Шаблоны пользователя',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=150, verbose_name='Номер договора')),
                ('content', models.TextField(verbose_name='Текст договора')),
                ('status', models.CharField(choices=[('CR', 'Создан'), ('SG', 'Подписан'), ('CL', 'Закрыт'), ('DS', 'Расторгнут'), ('EX', 'Истек')], default='CR', max_length=2, verbose_name='Статус договора')),
                ('deal_amount', models.IntegerField(default=0, verbose_name='Сумма сделки')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата заключения договора')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания договора')),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=160, verbose_name='Номер Дополнения')),
                ('title', models.CharField(max_length=150, verbose_name='Название дополнения')),
                ('content', models.TextField(verbose_name='Текст дополнения')),
                ('deal_amount', models.IntegerField(default=0, verbose_name='Сумма сделки')),
                ('status', models.CharField(choices=[('CR', 'Создан'), ('CL', 'Закрыт')], default='CR', max_length=2, verbose_name='Статус Дополнения')),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=160, verbose_name='Номер Акта')),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=160, verbose_name='Номер Чека')),
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
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=160, verbose_name='Номер Счета')),
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
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('IN', 'Инициирован'), ('CL', 'Проведен')], default='IN', max_length=2, verbose_name='Статус счета')),
                ('act', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='documents.act', verbose_name='Акт')),
                ('additional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='documents.additional', verbose_name='Дополнение')),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='documents.agreement', verbose_name='Договор')),
                ('check_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='documents.checkmodel', verbose_name='Чек')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='documents.invoice', verbose_name='Счет')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
    ]
