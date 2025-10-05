data = SqlHelper.GetList("SELECT * FROM sys_ProductConfigurations")
data = SqlHelper.GetList("SELECT * FROM sys_ProductSalesUnitOfMeasure")
data = SqlHelper.GetList("SELECT * FROM ProductAuditTrail")
data = SqlHelper.GetList("SELECT * FROM product_versions")

query = SqlHelper.GetList("SELECT pv.is_active, pv.product_id,puom.Denominator,puom.Numerator,puom.Unit FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON (pv.product_system_id = puom.ProductSystemId) WHERE is_active = '{0}' and product_id = '{1}'".format(True,'5150'))


LBF_QC_RAIL_SELLPRICE

# This script is for Rail Simple products to fetch cost from VCP/CPS/LIST_PRICE and update in the SELLRPICE/UNIT
for item in context.AffectedItems:
    if item["LBF_QU_SalesOrg"] == "3000":
        #Trace.Write("CPS Pricing to Work")
        if item.ListPrice > 0:
            item["LBF_QU_SELPRICE_UN"] = item.ListPrice
            item["LBF_QU_SELPRICE"] = item.ListPrice * item.Quantity



for item in context.Quote.GetAllItems():
    Trace.Write(item.AsMainItem.UnitOfMeasure)
    uom = item.AsMainItem.UnitOfMeasure
    material = item.PartNumber
    plant = item['LBF_QU_PLANT1']
    sqlquery = "select DC, DIV, SORG, Plant, SAP_COST, PRICE_UNIT from LBF_QU_MAT_COST where Material like '%{0}' and Plant = '{1}' ".format(str(material), str(plant))
    result = SqlHelper.GetFirst(sqlquery)
    uomdata = SqlHelper.GetFirst("SELECT pv.is_active, pv.product_id,puom.Denominator,puom.Numerator,puom.Unit FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON (pv.product_system_id = puom.ProductSystemId) WHERE is_active = '{0}' and product_id = '{1}' and Unit ='{2}'".format(True,str(item.ProductId),uom))
    if uomdata:
        if uom != 'FOT':
            item['LBF_QU_ExtCost'] = item['LBF_QU_MAT_CST'] * (item.Quantity * (uomdata.Denominator / uomdata.Numerator))
        else:
            item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT)
            item['LBF_QU_ExtCost'] = item['LBF_QU_MAT_CST'] * item.Quantity
            #item['LBF_QU_ExtCost'] = item['LBF_QU_MAT_CST'] * (item.Quantity * (queruomdatay.Numerator / uomdata.Denominator))


for item in context.Quote.GetAllItems():
#for item in context.AffectedItems:
    Trace.Write(item["LBF_QU_SalesOrg"])
    if item["LBF_QU_SalesOrg"] == "1000":
        #Trace.Write("CPS Pricing to Work")
        if item.ListPrice >= 0:
            item["LBF_QU_SELPRICE_UN"] = item.ListPrice
            item["LBF_QU_SELPRICE"] = item.ListPrice * item.Quantity



for item in context.Quote.GetAllItems():
    Log.Info('LBF_GS_RAIL_PRECAST_SELLPRICE--->')
    if item["LBF_QU_SalesOrg"] == "1000":
        Log.Info("111")
        if item.ListPrice >= 0:
            Log.Info("222")
            item["LBF_QU_SELPRICE_UN"] = item.ListPrice
            item["LBF_QU_SELPRICE"] = item.ListPrice * item.Quantity
    elif item["LBF_QU_SalesOrg"] == "3000":
        Log.Info("333")
        if item.ListPrice >= 0:
            Log.Info("444")
            item["LBF_QU_SELPRICE_UN"] = item.ListPrice
            item["LBF_QU_SELPRICE"] = item.ListPrice * item.Quantity
            item["LBF_QU_ExtCost"] = item['LBF_QU_MAT_CST'] * item.Quantity