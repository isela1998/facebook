# Generated by Django 3.1.1 on 2021-03-22 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0138_detbudget_subtotal_dl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datejoined', models.DateField(default='2021-03-22', max_length=10, verbose_name='Fecha')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=30)),
                ('facilitator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crud.facilitator', verbose_name='Facilitador')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crud.providers', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
                'ordering': ['id'],
            },
        ),
    ]
