// >>>>>>>>>>>>>>>>>>>>
SELECT Invoice_invoice.id, Invoice_invoice.CardCode, Invoice_invoice.CardName, sum(Invoice_invoice.DocTotal - Invoice_invoice.PaidToDateSys) as `DocTotal` FROM Invoice_invoice WHERE Invoice_invoice.DocumentStatus = 'bost_Open' AND Invoice_invoice.CancelStatus = 'csNo' GROUP BY Invoice_invoice.CardCode;
// >>>>>>>>>>>>>>>>>>>>

// >>>>>>>>>>>>>>>>>>>>
SELECT Invoice_invoice.id, Invoice_invoice.CardCode, Invoice_invoice.CardName, sum(Invoice_invoice.DocTotal - Invoice_invoice.PaidToDateSys) as `DocTotal` FROM Invoice_invoice RIGHT JOIN BusinessPartner_businesspartner ON BusinessPartner_businesspartner.CardCode = Invoice_invoice.CardCode WHERE Invoice_invoice.DocumentStatus = 'bost_Open' AND Invoice_invoice.CancelStatus = 'csNo' GROUP BY Invoice_invoice.CardCode;
// >>>>>>>>>>>>>>>>>>>>

// >>>>>>>>>>>>>>>>>>>>
SELECT BusinessPartner_businesspartner.id, BusinessPartner_businesspartner.CardCode, BusinessPartner_businesspartner.CardName, sum(Invoice_invoice.DocTotal - Invoice_invoice.PaidToDateSys) as `DocTotal` 
FROM BusinessPartner_businesspartner
INNER JOIN Invoice_invoice 
ON BusinessPartner_businesspartner.CardCode = Invoice_invoice.CardCode 
WHERE 
Invoice_invoice.DocumentStatus = 'bost_Open' 
AND Invoice_invoice.CancelStatus = 'csNo' 
GROUP BY Invoice_invoice.CardCode;
// >>>>>>>>>>>>>>>>>>>>
SELECT
    bp.id,
    bp.CardCode,
    bp.CardName,
    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `DocTotal`,
    IFNULL(COUNT(inv.DocEntry), 0) AS InvCount
FROM BusinessPartner_businesspartner bp
LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
    AND inv.DocumentStatus = 'bost_Open' 
    AND inv.CancelStatus = 'csNo'
GROUP BY bp.CardCode;
// >>>>>>>>>>>>>>>>>>>>
SELECT
    bp.id,
    bp.CardCode,
    bp.CardName,
    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `DocTotal`,
    IFNULL(COUNT(inv.DocEntry), 0) AS InvCount,
    SUM(IFNULL(DATEDIFF(invpay.DocDate, inv.DocDate), 0)) AS payDays
FROM BusinessPartner_businesspartner bp
LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
LEFT JOIN Invoice_incomingpaymentinvoices invpay ON inv.DocEntry = invpay.InvoiceDocEntry
    AND inv.DocumentStatus = 'bost_Open' 
    AND inv.CancelStatus = 'csNo'
GROUP BY bp.CardCode
// >>>>>>>>>>>>>>>>>>>>
SELECT
    bp.id,
    bp.CardCode,
    bp.CardName,
    IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
    IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`,
    IFNULL(COUNT(inv.DocEntry), 0) AS InvCount,
    IFNULL(COUNT(invpay.id), 0) AS InvPayCount,
    SUM(IFNULL(DATEDIFF(invpay.DocDate, inv.DocDate), 0)) AS payDays
FROM BusinessPartner_businesspartner bp
LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
LEFT JOIN Invoice_incomingpaymentinvoices invpay ON inv.DocEntry = invpay.InvoiceDocEntry
    AND inv.DocumentStatus = 'bost_Open' 
    AND inv.CancelStatus = 'csNo'
GROUP BY bp.CardCode

//>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>

SELECT
    bp.GroupCode,
    IFNULL(bpgroup.Name, '') as GroupName,
    IFNULL(SUM(inv.DocTotal), 0) AS `DocTotal`,
    IFNULL(SUM(inv.PaidToDateSys), 0) AS `PaidToDateSys`,
    IFNULL(SUM(inv.DocTotal - inv.PaidToDateSys), 0) AS `PendingTotal`
FROM BusinessPartner_businesspartner bp
LEFT JOIN BusinessPartner_businesspartnergroups bpgroup ON bpgroup.Code = bp.GroupCode
LEFT JOIN Invoice_invoice inv ON bp.CardCode = inv.CardCode
    AND inv.DocumentStatus = 'bost_Open' 
    AND inv.CancelStatus = 'csNo'
GROUP BY bp.GroupCode