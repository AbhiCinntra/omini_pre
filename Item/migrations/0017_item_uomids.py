# Generated by Django 4.0.3 on 2023-02-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0016_item_salesitemsperunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='UoMIds',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
