# Generated by Django 4.0.3 on 2023-06-22 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InvoiceID', models.CharField(blank=True, max_length=5)),
                ('BillToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToState', models.CharField(blank=True, max_length=100)),
                ('BillToCity', models.CharField(blank=True, max_length=100)),
                ('ShipToCountry', models.CharField(blank=True, max_length=100)),
                ('BillToZipCode', models.CharField(blank=True, max_length=100)),
                ('ShipToStreet', models.CharField(blank=True, max_length=100)),
                ('BillToState', models.CharField(blank=True, max_length=100)),
                ('ShipToZipCode', models.CharField(blank=True, max_length=100)),
                ('BillToStreet', models.CharField(blank=True, max_length=100)),
                ('ShipToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToCity', models.CharField(blank=True, max_length=100)),
                ('BillToCountry', models.CharField(blank=True, max_length=100)),
                ('U_SCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SSTATE', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPB', models.CharField(blank=True, max_length=100)),
                ('U_BSTATE', models.CharField(blank=True, max_length=100)),
                ('U_BCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPS', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineNum', models.IntegerField(default=0)),
                ('InvoiceID', models.CharField(blank=True, max_length=5)),
                ('Quantity', models.IntegerField(default=0)),
                ('UnitPrice', models.FloatField(default=0)),
                ('DiscountPercent', models.FloatField(default=0)),
                ('ItemDescription', models.CharField(blank=True, max_length=150)),
                ('ItemCode', models.CharField(blank=True, max_length=10)),
                ('TaxCode', models.CharField(blank=True, max_length=10)),
                ('BaseEntry', models.CharField(blank=True, default='', max_length=10)),
                ('TaxRate', models.CharField(blank=True, default=0, max_length=10)),
                ('UomNo', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseCreditNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InvoiceDocEntry', models.CharField(blank=True, max_length=10)),
                ('DocEntry', models.CharField(blank=True, max_length=10)),
                ('CardCode', models.CharField(blank=True, max_length=50)),
                ('CardName', models.CharField(blank=True, max_length=250)),
                ('DocDate', models.CharField(blank=True, max_length=100)),
                ('DocTotal', models.CharField(blank=True, max_length=100)),
                ('SalesPersonCode', models.CharField(blank=True, max_length=100)),
                ('Comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaxDate', models.CharField(blank=True, max_length=30)),
                ('DocDueDate', models.CharField(blank=True, max_length=30)),
                ('ContactPersonCode', models.CharField(blank=True, max_length=5)),
                ('DiscountPercent', models.CharField(blank=True, max_length=5)),
                ('DocDate', models.CharField(blank=True, max_length=30)),
                ('CardCode', models.CharField(blank=True, max_length=30)),
                ('Comments', models.TextField(blank=True)),
                ('SalesPersonCode', models.CharField(blank=True, max_length=5)),
                ('DocumentStatus', models.CharField(blank=True, max_length=50)),
                ('DocCurrency', models.CharField(blank=True, max_length=50)),
                ('DocTotal', models.CharField(blank=True, max_length=50)),
                ('CardName', models.CharField(blank=True, max_length=250)),
                ('VatSum', models.CharField(blank=True, max_length=50)),
                ('CreationDate', models.CharField(blank=True, max_length=50)),
                ('DocEntry', models.CharField(blank=True, max_length=5)),
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('AdditionalCharges', models.CharField(blank=True, max_length=100)),
                ('DeliveryCharge', models.CharField(blank=True, max_length=100)),
                ('CreateDate', models.CharField(blank=True, max_length=30)),
                ('CreateTime', models.CharField(blank=True, max_length=30)),
                ('UpdateDate', models.CharField(blank=True, max_length=30)),
                ('UpdateTime', models.CharField(blank=True, max_length=30)),
                ('PaymentGroupCode', models.CharField(blank=True, default=1, max_length=100)),
                ('Series', models.CharField(blank=True, default='241', max_length=100)),
                ('CancelStatus', models.CharField(blank=True, default='csNo', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DocNum', models.CharField(blank=True, max_length=100)),
                ('DocType', models.CharField(blank=True, max_length=100)),
                ('DocDate', models.CharField(blank=True, max_length=100)),
                ('CardCode', models.CharField(blank=True, max_length=100)),
                ('CardName', models.CharField(blank=True, max_length=250)),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('DocCurrency', models.CharField(blank=True, max_length=100)),
                ('CheckAccount', models.CharField(blank=True, max_length=100)),
                ('TransferAccount', models.CharField(blank=True, max_length=100)),
                ('TransferSum', models.CharField(blank=True, max_length=100)),
                ('TransferDate', models.CharField(blank=True, max_length=100)),
                ('TransferReference', models.CharField(blank=True, max_length=100)),
                ('Series', models.CharField(blank=True, max_length=100)),
                ('DocEntry', models.CharField(blank=True, max_length=100)),
                ('DueDate', models.CharField(blank=True, max_length=100)),
                ('BPLID', models.CharField(blank=True, max_length=100)),
                ('BPLName', models.CharField(blank=True, max_length=100)),
                ('Comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPaymentsInvoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VendorPaymentsId', models.CharField(blank=True, max_length=10)),
                ('LineNum', models.CharField(blank=True, max_length=100)),
                ('InvoiceDocEntry', models.CharField(blank=True, max_length=100)),
                ('SumApplied', models.CharField(blank=True, max_length=100)),
                ('AppliedFC', models.CharField(blank=True, max_length=100)),
                ('AppliedSys', models.CharField(blank=True, max_length=100)),
                ('DiscountPercent', models.CharField(blank=True, max_length=100)),
                ('TotalDiscount', models.CharField(blank=True, max_length=100)),
                ('TotalDiscountFC', models.CharField(blank=True, max_length=100)),
                ('TotalDiscountSC', models.CharField(blank=True, max_length=100)),
                ('DocDate', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]