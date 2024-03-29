# Generated by Django 4.0.3 on 2023-04-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(blank=True, max_length=200)),
                ('JdtNum', models.CharField(blank=True, max_length=200)),
                ('Original', models.CharField(blank=True, max_length=200)),
                ('OriginalJournal', models.CharField(blank=True, max_length=200)),
                ('ReferenceDate', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntryLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JournalEntriesId', models.CharField(blank=True, max_length=30)),
                ('Line_ID', models.CharField(blank=True, max_length=200)),
                ('AccountCode', models.CharField(blank=True, max_length=200)),
                ('Debit', models.CharField(blank=True, max_length=200)),
                ('Credit', models.CharField(blank=True, max_length=250)),
                ('DueDate', models.CharField(blank=True, max_length=250)),
                ('ShortName', models.CharField(blank=True, max_length=250)),
                ('ContraAccount', models.CharField(blank=True, max_length=250)),
                ('LineMemo', models.CharField(blank=True, max_length=250)),
                ('ReferenceDate1', models.CharField(blank=True, max_length=250)),
                ('Reference1', models.CharField(blank=True, max_length=250)),
            ],
        ),
    ]
