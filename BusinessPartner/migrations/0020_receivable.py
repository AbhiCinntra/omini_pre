# Generated by Django 3.2.19 on 2023-10-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0019_auto_20230627_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receivable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CardCode', models.CharField(blank=True, max_length=200)),
                ('CardName', models.CharField(blank=True, max_length=200)),
                ('SalesEmployeeCode', models.CharField(blank=True, max_length=200)),
                ('U_U_UTL_Zone', models.CharField(blank=True, max_length=200)),
                ('GroupCode', models.CharField(blank=True, max_length=200)),
                ('GroupName', models.CharField(blank=True, max_length=200)),
                ('DocEntry', models.CharField(blank=True, max_length=200)),
                ('TransId', models.CharField(blank=True, max_length=200)),
                ('TransType', models.CharField(blank=True, max_length=200)),
                ('OB', models.CharField(blank=True, max_length=200)),
                ('Debit', models.CharField(blank=True, max_length=200)),
                ('Credit', models.CharField(blank=True, max_length=200)),
                ('CB', models.CharField(blank=True, max_length=200)),
                ('TotalDue', models.CharField(blank=True, max_length=200)),
                ('DueDaysGroup', models.CharField(blank=True, max_length=200)),
                ('DocDate', models.CharField(blank=True, max_length=200)),
                ('DueDate', models.CharField(blank=True, max_length=200)),
                ('CronUpdateCount', models.CharField(blank=True, default=1, max_length=200)),
                ('Datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
