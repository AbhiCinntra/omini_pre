# Generated by Django 3.2.13 on 2023-02-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0011_itempricelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='U_GST',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
