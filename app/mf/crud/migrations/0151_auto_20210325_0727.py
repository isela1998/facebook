# Generated by Django 3.1.1 on 2021-03-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0150_invoices_number_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detinvoices',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Cantidad'),
        ),
    ]