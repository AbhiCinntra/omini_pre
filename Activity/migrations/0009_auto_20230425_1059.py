# Generated by Django 3.2.13 on 2023-04-25 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0008_maps_attach'),
    ]

    operations = [
        migrations.AddField(
            model_name='maps',
            name='ExpenseAttach',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='maps',
            name='ExpenseCost',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='maps',
            name='ExpenseDistance',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='maps',
            name='ExpenseRemark',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='maps',
            name='ExpenseType',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]