# Generated by Django 3.2.7 on 2022-03-09 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0006_item_uom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='UoM',
            new_name='UoS',
        ),
    ]
