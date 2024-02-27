# Generated by Django 3.2.19 on 2023-09-22 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0005_alter_documentlines_itemdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditnotes',
            name='AdditionalCharges',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CancelStatus',
            field=models.CharField(blank=True, default='csNo', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CardCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CardName',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='ContactPersonCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CreateDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CreateTime',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='CreationDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DeliveryCharge',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DiscountPercent',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocCurrency',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocDueDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocEntry',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocNum',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocTotal',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='DocumentStatus',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='InvoiceDocEntry',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='OrderID',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='PaymentGroupCode',
            field=models.CharField(blank=True, default=1, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='SalesPersonCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='Series',
            field=models.CharField(blank=True, default='241', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='TaxDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='UpdateDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='UpdateTime',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotes',
            name='VatSum',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='BaseEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='HSNEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='ItemCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='ItemDescription',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='LineTotal',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='MeasureUnit',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='SACEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='TaxCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='TaxRate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_RateType',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_DD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_DIST',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_MRPI',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_SD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_SP',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='U_UTL_TD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='creditnotesdocumentlines',
            name='UomNo',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='BaseEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='HSNEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='ItemCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='LineTotal',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='MeasureUnit',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='SACEntry',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='TaxCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='TaxRate',
            field=models.CharField(blank=True, default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_RateType',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_DD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_DIST',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_MRPI',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_SD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_SP',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='U_UTL_TD',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='documentlines',
            name='UomNo',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='AdditionalCharges',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CancelStatus',
            field=models.CharField(blank=True, default='csNo', max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CardCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CardName',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='ContactPersonCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CreateDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CreateTime',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='CreationDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DeliveryCharge',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DiscountPercent',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocCurrency',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocDueDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocEntry',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocNum',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocTotal',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='DocumentStatus',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='OrderID',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='PaymentGroupCode',
            field=models.CharField(blank=True, default=1, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='SalesPersonCode',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='Series',
            field=models.CharField(blank=True, default='241', max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='TaxDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='UpdateDate',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='UpdateTime',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='VatSum',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]