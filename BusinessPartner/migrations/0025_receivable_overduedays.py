# Generated by Django 3.2.19 on 2023-10-20 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0024_alter_receivable_cronupdatecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivable',
            name='OverDueDays',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]