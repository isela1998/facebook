# Generated by Django 3.1.1 on 2021-03-25 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0151_auto_20210325_0727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dollarhistory',
            name='rate_dolar2',
        ),
    ]
