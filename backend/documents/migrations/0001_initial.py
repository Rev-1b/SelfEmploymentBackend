# Generated by Django 5.0.6 on 2024-05-29 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название дополнения')),
                ('content', models.TextField(verbose_name='Текст дополнения')),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_number', models.CharField(max_length=16, verbose_name='Номер договора')),
                ('content', models.TextField(verbose_name='Текст договора')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='customers.customer', verbose_name='Договоры')),
            ],
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('baseattachment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.baseattachment')),
                ('title', models.CharField(max_length=150, verbose_name='Название акта')),
                ('content', models.TextField(verbose_name='Текст акта')),
            ],
            bases=('documents.baseattachment',),
        ),
        migrations.CreateModel(
            name='CheckModel',
            fields=[
                ('baseattachment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.baseattachment')),
                ('amount', models.IntegerField(verbose_name='Сумма')),
            ],
            bases=('documents.baseattachment',),
        ),
        migrations.AddField(
            model_name='baseattachment',
            name='additional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_attachment', to='documents.additional'),
        ),
        migrations.AddField(
            model_name='baseattachment',
            name='agreement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_attachment', to='documents.agreement'),
        ),
        migrations.AddField(
            model_name='additional',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional', to='documents.agreement', verbose_name='Дополнения к договору'),
        ),
    ]
