# Generated by Django 3.2.13 on 2023-03-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunity', '0009_auto_20230307_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='oppitem',
            name='UnitPriceown',
            field=models.CharField(blank=True, default=0, max_length=5),
        ),
    ]
