# Generated by Django 4.2.13 on 2024-07-02 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
