# Generated by Django 4.1.6 on 2023-02-05 18:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_transactions_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 12, 23, 34, 22, 711372)),
        ),
    ]