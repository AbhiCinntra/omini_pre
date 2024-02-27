# Generated by Django 4.1.6 on 2024-02-12 11:33

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
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('ShipToStreet', models.CharField(blank=True, max_length=100)),
                ('ShipToBlock', models.CharField(blank=True, max_length=100)),
                ('ShipToBuilding', models.CharField(blank=True, max_length=100)),
                ('ShipToCity', models.CharField(blank=True, max_length=100)),
                ('ShipToZipCode', models.CharField(blank=True, max_length=100)),
                ('ShipToCounty', models.CharField(blank=True, max_length=100)),
                ('ShipToState', models.CharField(blank=True, max_length=100)),
                ('ShipToCountry', models.CharField(blank=True, max_length=100)),
                ('ShipToAddress2', models.CharField(blank=True, max_length=100)),
                ('ShipToAddress3', models.CharField(blank=True, max_length=100)),
                ('BillToStreet', models.CharField(blank=True, max_length=100)),
                ('BillToBlock', models.CharField(blank=True, max_length=100)),
                ('BillToBuilding', models.CharField(blank=True, max_length=100)),
                ('BillToCity', models.CharField(blank=True, max_length=100)),
                ('BillToZipCode', models.CharField(blank=True, max_length=100)),
                ('BillToCounty', models.CharField(blank=True, max_length=100)),
                ('BillToState', models.CharField(blank=True, max_length=100)),
                ('BillToCountry', models.CharField(blank=True, max_length=100)),
                ('BillToAddress2', models.CharField(blank=True, max_length=100)),
                ('BillToAddress3', models.CharField(blank=True, max_length=100)),
                ('PlaceOfSupply', models.CharField(blank=True, max_length=100)),
                ('U_SCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SSTATE', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPB', models.CharField(blank=True, max_length=100)),
                ('U_BSTATE', models.CharField(blank=True, max_length=100)),
                ('U_BCOUNTRY', models.CharField(blank=True, max_length=100)),
                ('U_SHPTYPS', models.CharField(blank=True, max_length=100)),
                ('PurchasePlaceOfSupply', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineNum', models.IntegerField(default=0)),
                ('OrderID', models.CharField(blank=True, max_length=5)),
                ('Quantity', models.IntegerField(default=0)),
                ('UnitPrice', models.FloatField(default=0)),
                ('DiscountPercent', models.FloatField(default=0)),
                ('ItemDescription', models.CharField(blank=True, max_length=200)),
                ('ItemCode', models.CharField(blank=True, max_length=200)),
                ('TaxCode', models.CharField(blank=True, max_length=200)),
                ('BaseEntry', models.CharField(blank=True, default='', max_length=200)),
                ('TaxRate', models.CharField(blank=True, default=0, max_length=200)),
                ('UomNo', models.CharField(blank=True, default='', max_length=200)),
                ('LineTotal', models.CharField(blank=True, default='', max_length=200)),
                ('MeasureUnit', models.CharField(blank=True, default='', max_length=100)),
                ('SACEntry', models.CharField(blank=True, default='', max_length=100)),
                ('HSNEntry', models.CharField(blank=True, default='', max_length=100)),
                ('SAC', models.CharField(blank=True, default='', max_length=250)),
                ('HSN', models.CharField(blank=True, default='', max_length=250)),
                ('U_UTL_DIST', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_SP', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_DD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_SD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_TD', models.CharField(blank=True, default='', max_length=100)),
                ('U_UTL_MRPI', models.CharField(blank=True, default='', max_length=100)),
                ('U_RateType', models.CharField(blank=True, default='', max_length=100)),
                ('RemainingOpenQuantity', models.CharField(blank=True, default=0, max_length=20)),
                ('OpenAmount', models.CharField(blank=True, default=0, max_length=100)),
                ('LineStatus', models.CharField(blank=True, default='bost_Open', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DocNum', models.CharField(blank=True, max_length=250)),
                ('DocEntry', models.CharField(blank=True, max_length=250)),
                ('CardCode', models.CharField(blank=True, max_length=250)),
                ('CardName', models.CharField(blank=True, max_length=250)),
                ('SalesPersonCode', models.CharField(blank=True, max_length=250)),
                ('TaxDate', models.CharField(blank=True, max_length=250)),
                ('DocDueDate', models.CharField(blank=True, max_length=250)),
                ('ContactPersonCode', models.CharField(blank=True, max_length=250)),
                ('DiscountPercent', models.CharField(blank=True, max_length=250)),
                ('DocDate', models.CharField(blank=True, max_length=250)),
                ('Comments', models.TextField(blank=True)),
                ('DocumentStatus', models.CharField(blank=True, max_length=250)),
                ('DocCurrency', models.CharField(blank=True, max_length=250)),
                ('DocTotal', models.CharField(blank=True, max_length=250)),
                ('VatSum', models.CharField(blank=True, max_length=250)),
                ('CreationDate', models.CharField(blank=True, max_length=250)),
                ('AdditionalCharges', models.CharField(blank=True, max_length=250)),
                ('DeliveryCharge', models.CharField(blank=True, max_length=250)),
                ('CreateDate', models.CharField(blank=True, max_length=250)),
                ('CreateTime', models.CharField(blank=True, max_length=250)),
                ('UpdateDate', models.CharField(blank=True, max_length=250)),
                ('UpdateTime', models.CharField(blank=True, max_length=250)),
                ('PaymentGroupCode', models.CharField(blank=True, default=1, max_length=100)),
                ('Series', models.CharField(blank=True, default='241', max_length=100)),
                ('CancelStatus', models.CharField(blank=True, default='csNo', max_length=100)),
                ('BPLID', models.CharField(blank=True, max_length=200)),
                ('BPLName', models.CharField(blank=True, max_length=200)),
                ('WTAmount', models.CharField(blank=True, max_length=200)),
                ('U_E_INV_NO', models.CharField(blank=True, max_length=200)),
                ('U_E_INV_Date', models.CharField(blank=True, max_length=200)),
                ('DocType', models.CharField(blank=True, default='dDocument_Items', max_length=100)),
                ('IGST', models.CharField(blank=True, default=0, max_length=200)),
                ('CGST', models.CharField(blank=True, default=0, max_length=200)),
                ('SGST', models.CharField(blank=True, default=0, max_length=200)),
                ('GSTRate', models.CharField(blank=True, default=0, max_length=200)),
                ('RoundingDiffAmount', models.CharField(blank=True, default=0, max_length=200)),
                ('U_SignedQRCode', models.TextField(blank=True, default='')),
                ('U_SignedInvoice', models.TextField(blank=True, default='')),
                ('U_EWayBill', models.TextField(blank=True, default='')),
                ('U_TransporterID', models.CharField(blank=True, default=0, max_length=200)),
                ('U_TransporterName', models.CharField(blank=True, default=0, max_length=200)),
                ('U_VehicalNo', models.CharField(blank=True, default=0, max_length=200)),
                ('NumAtCard', models.CharField(blank=True, default=0, max_length=200)),
                ('U_UNE_LRNo', models.CharField(blank=True, default=0, max_length=200)),
                ('U_UNE_LRDate', models.CharField(blank=True, default=0, max_length=200)),
                ('U_UNE_IRN', models.TextField(blank=True, default='')),
                ('CNNo', models.TextField(blank=True, default='')),
                ('Address', models.TextField(blank=True, default='')),
                ('Address2', models.TextField(blank=True, default='')),
                ('VATRegNum', models.TextField(blank=True, default='')),
            ],
        ),
    ]