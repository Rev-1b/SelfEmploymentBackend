# Generated by Django 5.0.6 on 2024-07-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_advertiseinfo_options_alter_passport_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Подтверждена почта'),
        ),
    ]
