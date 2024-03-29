# Generated by Django 3.2.19 on 2023-07-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JournalEntries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentries',
            name='CNNo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='journalentries',
            name='DocType',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='journalentries',
            name='Memo',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='journalentries',
            name='TaxDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='journalentries',
            name='TransactionCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='journalentries',
            name='U_UNE_Narration',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='journalentrylines',
            name='AccountName',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='journalentrylines',
            name='BPLID',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='journalentrylines',
            name='BPLName',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='journalentrylines',
            name='Reference2',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='journalentrylines',
            name='LineMemo',
            field=models.TextField(blank=True),
        ),
    ]
