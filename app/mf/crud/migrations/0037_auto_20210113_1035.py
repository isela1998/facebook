# Generated by Django 3.1.1 on 2021-01-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0036_auto_20210113_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movingproducts',
            name='datejoined',
            field=models.DateField(default='2021-01-13', max_length=50, verbose_name='Fecha'),
        ),
    ]
