for item in context.AffectedItems:
    Trace.Write(item.AsMainItem.UnitOfMeasure)
    uom = item.AsMainItem.UnitOfMeasure
    material = item.PartNumber
    vcpProCheck = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(material,'True','True'))
    if vcpProCheck:
        plant = item['LBF_QU_PLANT1']
        sqlquery = "select DC, DIV, SORG, Plant, SAP_COST, PRICE_UNIT from LBF_QU_MAT_COST where Material like '%{0}' and Plant = '{1}' ".format(str(material), str(plant))
        result = SqlHelper.GetFirst(sqlquery)
        uomdata = SqlHelper.GetFirst("SELECT pv.is_active, pv.product_id, puom.Denominator, puom.Numerator, puom.Unit, pr.UnitOfMeasure FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON pv.product_system_id = puom.ProductSystemId INNER JOIN PRODUCTS pr ON pv.product_id = pr.PRODUCT_ID WHERE pv.is_active = '{0}' AND pv.product_id = '{1}' AND puom.Unit = '{2}'".format(True, str(item.ProductId), uom))
        if uomdata:
            if uom != str(uomdata.UnitOfMeasure):
                item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT) * (float(uomdata.Numerator) / float(uomdata.Denominator))
                item['LBF_QU_ExtCost'] = float(item['LBF_QU_MAT_CST']) * float(item.Quantity)
            else:
                item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT)
                item['LBF_QU_ExtCost'] = float(item['LBF_QU_MAT_CST']) * float(item.Quantity)