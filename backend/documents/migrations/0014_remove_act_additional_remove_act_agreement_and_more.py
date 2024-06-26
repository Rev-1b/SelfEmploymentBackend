# Generated by Django 5.0.6 on 2024-06-25 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0013_payment_alter_act_options_alter_additional_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='act',
            name='additional',
        ),
        migrations.RemoveField(
            model_name='act',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='additional',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='checkmodel',
            name='additional',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='additional',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='checkmodel',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='agreement',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.RemoveField(
            model_name='usertemplate',
            name='user',
        ),
        migrations.DeleteModel(
            name='Act',
        ),
        migrations.DeleteModel(
            name='Additional',
        ),
        migrations.DeleteModel(
            name='Deal',
        ),
        migrations.DeleteModel(
            name='CheckModel',
        ),
        migrations.DeleteModel(
            name='Agreement',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='UserTemplate',
        ),
    ]