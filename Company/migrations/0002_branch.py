# Generated by Django 4.0.3 on 2023-02-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BPLId', models.CharField(max_length=5)),
                ('BPLName', models.CharField(blank=True, max_length=250)),
                ('Address', models.CharField(blank=True, max_length=250)),
                ('MainBPL', models.CharField(blank=True, max_length=5)),
                ('Disabled', models.CharField(blank=True, max_length=5)),
                ('UserSign2', models.CharField(blank=True, max_length=5)),
                ('UpdateDate', models.CharField(blank=True, max_length=50)),
                ('DflWhs', models.CharField(blank=True, max_length=50)),
                ('TaxIdNum', models.CharField(blank=True, max_length=100)),
                ('StreetNo', models.CharField(blank=True, max_length=100)),
                ('Building', models.CharField(blank=True, max_length=100)),
                ('ZipCode', models.CharField(blank=True, max_length=100)),
                ('City', models.CharField(blank=True, max_length=100)),
                ('State', models.CharField(blank=True, max_length=100)),
                ('Country', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
