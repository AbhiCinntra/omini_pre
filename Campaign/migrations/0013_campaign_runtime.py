# Generated by Django 3.2.13 on 2022-08-01 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0012_alter_campaign_monthlydate'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='RunTime',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
