# Generated by Django 3.1.7 on 2021-04-03 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='income',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='income_currency',
        ),
    ]
