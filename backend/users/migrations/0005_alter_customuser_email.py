# Generated by Django 5.0.6 on 2024-06-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Электронный адрес'),
        ),
    ]