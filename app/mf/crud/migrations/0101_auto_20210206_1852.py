# Generated by Django 3.1.1 on 2021-02-06 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0100_auto_20210206_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debts',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Tasa(Bs.)'),
        ),
    ]