# Generated by Django 3.2.13 on 2023-03-07 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0014_businesspartner_createdfromsap'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesspartner',
            name='CurrentAccountBalance',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='businesspartner',
            name='OpenChecksBalance',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='businesspartner',
            name='OpenDeliveryNotesBalance',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='businesspartner',
            name='OpenOrdersBalance',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
    ]