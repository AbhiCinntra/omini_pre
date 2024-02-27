# Generated by Django 3.2.13 on 2022-10-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0002_bptype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.CharField(blank=True, max_length=150)),
                ('CreateDate', models.CharField(blank=True, max_length=100)),
                ('CreateTime', models.CharField(blank=True, max_length=100)),
                ('UpdateDate', models.CharField(blank=True, max_length=100)),
                ('UpdateTime', models.CharField(blank=True, max_length=100)),
                ('CustId', models.IntegerField(default=0)),
            ],
        ),
    ]
