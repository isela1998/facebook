# Generated by Django 3.1.1 on 2021-02-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0071_auto_20210201_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changescanceled',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=30, verbose_name='Cantidad ($$ ó Bs.)'),
        ),
    ]
