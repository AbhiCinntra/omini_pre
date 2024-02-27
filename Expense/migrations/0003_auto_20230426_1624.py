# Generated by Django 3.2.13 on 2023-04-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0002_expense_employeeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='endLat',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='endLong',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='startLat',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='startLong',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='travelDistance',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]