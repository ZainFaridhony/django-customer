# Generated by Django 3.1.7 on 2021-04-05 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20210405_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='income_int',
            field=models.IntegerField(null=True),
        ),
    ]