# Generated by Django 3.1.1 on 2021-02-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0085_auto_20210204_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransfers',
            name='description',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='Notas y/o Descripción'),
        ),
    ]
