# Generated by Django 3.1.1 on 2020-12-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0013_auto_20201220_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='received',
            field=models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Entrada'),
        ),
    ]
