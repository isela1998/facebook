# Generated by Django 3.1.1 on 2021-03-24 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0147_invoices_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
