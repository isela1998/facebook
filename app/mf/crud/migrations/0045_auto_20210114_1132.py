# Generated by Django 3.1.1 on 2021-01-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0044_auto_20210114_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movingproducts',
            name='datejoined',
            field=models.DateField(default='2021-01-14', max_length=50, verbose_name='Fecha'),
        ),
    ]