# Generated by Django 5.0.6 on 2024-06-23 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_passport_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='passport',
            unique_together=set(),
        ),
    ]
