# Generated by Django 3.1.1 on 2021-02-23 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0122_auto_20210223_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='category',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='category',
            name='user_creation',
        ),
        migrations.RemoveField(
            model_name='category',
            name='user_updated',
        ),
    ]
