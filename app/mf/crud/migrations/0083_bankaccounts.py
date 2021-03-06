# Generated by Django 3.1.1 on 2021-02-04 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0082_banktransfers_pay_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=255, verbose_name='Nombre del Banco')),
                ('accountHolder', models.CharField(max_length=255, verbose_name='Titular de la Cuenta')),
                ('holderId', models.CharField(max_length=255, verbose_name='Cédula/RIF Titular')),
                ('accountNumber', models.CharField(max_length=255, verbose_name='Número de Cuenta')),
            ],
            options={
                'verbose_name': 'Cuenta Bancaria',
                'verbose_name_plural': 'Cuentas Bancarias',
                'ordering': ['id'],
            },
        ),
    ]
