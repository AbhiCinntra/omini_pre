# Generated by Django 3.2.7 on 2022-02-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Warehouse', '0004_alter_inventory_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='ItemID',
        ),
        migrations.AddField(
            model_name='inventory',
            name='ItemCode',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
