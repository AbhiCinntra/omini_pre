# Generated by Django 3.2.19 on 2023-08-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryNote', '0002_alter_deliverynote_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverynote',
            name='CancelStatus',
            field=models.CharField(blank=True, default='csNo', max_length=100),
        ),
    ]
