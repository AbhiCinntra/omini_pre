# Generated by Django 3.2.7 on 2022-04-13 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_alter_maps_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatter',
            name='Mode',
            field=models.CharField(blank=True, max_length=10),
        )
    ]
