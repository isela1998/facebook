# Generated by Django 3.1.1 on 2021-03-23 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0142_remove_invoices_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='Ninguna', max_length=180, verbose_name='Descripción'),
        ),
    ]
