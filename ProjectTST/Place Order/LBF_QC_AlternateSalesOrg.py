items = context.AffectedItems

for item in items:
    material = item.PartNumber
    vcpProCheck = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(material,'True','True'))
    if vcpProCheck:
        plant = item['LBF_QU_PLANT1']
        query = "select DC, DIV, SORG, Plant, SAP_COST, PRICE_UNIT from LBF_QU_MAT_COST where Material like '%{0}' and Plant = '{1}' ".format(str(material), str(plant))
        result = SqlHelper.GetFirst(query)
        Log.Info('calling the data - > ' + str(material))
        if result:
            item['LBF_QU_PLANT1'] = result.Plant
            item['LBF_QU_DC'] = result.DC
            item['LBF_QU_SalesOrg'] = result.SORG
            Log.Info('Sales org is ->' + str(result.SORG))
            item['LBF_QU_PLANT'] = result.Plant
            Log.Info(str(result.DIV))
            item['LBF_QU_DIV'] = result.DIV if result.DIV else 0
            if item.ProductName != 'CWR' and item.ProductName != 'CWR_QI':
                item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT)
                item['LBF_QU_ExtCost'] = item['LBF_QU_MAT_CST'] * item.Quantity