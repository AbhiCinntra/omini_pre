# Generated by Django 3.2.13 on 2022-07-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunity', '0005_alter_opportunity_u_fav'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpportunityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]