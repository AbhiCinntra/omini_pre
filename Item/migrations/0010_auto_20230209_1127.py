# Generated by Django 3.2.13 on 2023-02-09 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0009_auto_20220729_0703'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PriceListNo', models.CharField(blank=True, max_length=200)),
                ('PriceListName', models.CharField(blank=True, max_length=200)),
                ('Currency', models.CharField(blank=True, max_length=200)),
                ('FixedAmount', models.CharField(blank=True, max_length=20)),
                ('Active', models.CharField(blank=True, default='tYES', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='Number',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AddField(
            model_name='item',
            name='ItemsGroupCode',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='CategoryName',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='CatID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Item.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='CodeType',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='Discount',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='HSN',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='Inventory',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='ItemCode',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='ItemName',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='item',
            name='Status',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='TaxCode',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='UnitPrice',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='tax',
            name='TaxCode',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
