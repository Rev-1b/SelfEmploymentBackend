# Generated by Django 5.0.6 on 2024-05-31 14:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_advertiseinfo_passport_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='advertise',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='passport',
        ),
        migrations.AddField(
            model_name='advertiseinfo',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='advertise_info', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passport',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='passport', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userrequisites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
