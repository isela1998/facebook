# Generated by Django 3.1.1 on 2021-01-22 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0059_auto_20210122_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='type_exchange',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='type_received',
        ),
        migrations.AddField(
            model_name='method_pay',
            name='type_symbol',
            field=models.CharField(default=2, max_length=150, verbose_name='Abreviación/Símbolo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='method_pay1',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='method_pay1', to='crud.method_pay', verbose_name='Método de pago (2)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='method_pay2',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='method_pay2', to='crud.method_pay', verbose_name='Método de pago (3)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='received1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=30, verbose_name='Entrada (2)'),
        ),
        migrations.AddField(
            model_name='sale',
            name='received2',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=30, verbose_name='Entrada (3)'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='method_pay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crud.method_pay', verbose_name='Método de pago (1)'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='received',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=30, verbose_name='Entrada (1)'),
        ),
    ]