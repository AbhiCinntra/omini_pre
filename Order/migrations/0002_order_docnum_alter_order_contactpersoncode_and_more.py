# Generated by Django 4.0.3 on 2024-02-21 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='DocNum',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='ContactPersonCode',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='CreatedBy',
            field=models.CharField(blank=True, default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='DiscountPercent',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='DocEntry',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='FreeDelivery',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]