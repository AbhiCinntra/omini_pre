# Generated by Django 3.2.13 on 2023-01-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='additionalCharges',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='deliveryMode',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='deliveryTerm',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='paymentType',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
