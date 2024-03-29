# Generated by Django 3.2.19 on 2023-08-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0002_auto_20230711_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalReconciliations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TransId', models.CharField(blank=True, max_length=100)),
                ('TransRowId', models.CharField(blank=True, max_length=100)),
                ('ReconType', models.CharField(blank=True, max_length=100)),
                ('ShortName', models.CharField(blank=True, max_length=100)),
                ('CancelAbs', models.CharField(blank=True, max_length=100)),
                ('Total', models.CharField(blank=True, max_length=100)),
                ('ReconDate', models.CharField(blank=True, max_length=100)),
                ('SrcObjAbs', models.CharField(blank=True, max_length=100)),
                ('SrcObjTyp', models.CharField(blank=True, max_length=100)),
                ('IsCredit', models.CharField(blank=True, max_length=100)),
                ('ReconNum', models.CharField(blank=True, max_length=100)),
                ('ReconSum', models.CharField(blank=True, max_length=100)),
                ('DueDate', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='creditnotes',
            name='PaidToDateSys',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='invoice',
            name='PaidToDateSys',
            field=models.TextField(blank=True, default=''),
        ),
    ]
