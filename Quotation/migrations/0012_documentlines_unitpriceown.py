# Generated by Django 3.2.13 on 2023-03-08 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0011_quotation_createdby'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentlines',
            name='UnitPriceown',
            field=models.CharField(blank=True, default=0, max_length=5),
        ),
    ]