# Generated by Django 3.2.13 on 2023-03-10 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0010_units_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='VenderCode',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]