# Generated by Django 3.2.19 on 2023-10-18 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0020_receivable'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivable',
            name='BPAddresses',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='ContactPerson',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='CreditLimit',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='CreditLimitDayes',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='EmailAddress',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='GSTIN',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='receivable',
            name='MobileNo',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
