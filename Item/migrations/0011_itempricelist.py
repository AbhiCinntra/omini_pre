# Generated by Django 3.2.13 on 2023-02-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0010_auto_20230209_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemCode', models.CharField(blank=True, max_length=100)),
                ('PriceList', models.CharField(blank=True, max_length=200)),
                ('Currency', models.CharField(blank=True, max_length=200)),
                ('Price', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
