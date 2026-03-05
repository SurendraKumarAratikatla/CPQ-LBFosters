def TargetUOM_Change(item,uom):
    taruom = item["LBF_QU_TARUOM"]
    try:
        new_uom = SqlHelper.GetFirst("select * from LBF_QU_UOM_MAPPING_FIELDS where S4CPI='{0}'".format(uom)).CPQDisplayUOM
    except:
        new_uom = uom

    if taruom:
        pass
    else:
        item["LBF_QU_TARUOM"] = new_uom

    if item["LBF_QU_TARUOM"]:
        if new_uom == "LB" and taruom.upper() not in ["TON", "KG"]:
            item["LBF_QU_TARUOM"] = "LB"

        elif new_uom != "LB":
            item["LBF_QU_TARUOM"] = new_uom


def UOMCheck():
    for item in context.Quote.GetAllItems():
        Log.Info(str(item.ProductName))
        #if item.ProductName != 'CWR_QI_320' or item.ProductName != 'CWR_QI': # CWR item check
        if item.ProductName != 'CWR_QI': #and item.ProductName != 'CWR_QI':
            Trace.Write(item.AsMainItem.UnitOfMeasure)
            # uom = item.AsMainItem.UnitOfMeasure
            # TargetUOM_Change(item,uom) # updating the target UOM based on Unit Of Meassure change
            # material = item.PartNumber
            # vcpProCheck = SqlHelper.GetFirst("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(material,'True','True'))
            # if vcpProCheck:
            #     plant = item['LBF_QU_PLANT1']
            #     sqlquery = "select DC, DIV, SORG, Plant,NET_WEIGHT,WEIGHT_UNIT, SAP_COST, PRICE_UNIT from LBF_QU_MAT_COST where Material like '%{0}' and Plant = '{1}' ".format(str(material), str(plant))
            #     result = SqlHelper.GetFirst(sqlquery)
            #     uomMapping = SqlHelper.GetFirst("SELECT S4CPI, CPQDisplayUOM from LBF_QU_UOM_MAPPING_FIELDS where S4CPI='{0}' or CPQDisplayUOM='{1}'".format(uom,uom))
            #     if uomMapping and result:
            #         if vcpProCheck.UnitOfMeasure != 'DR':
            #             Trace.Write(item.ProductId)
            #             uomdata = SqlHelper.GetFirst("SELECT pv.is_active, pv.product_id, puom.Denominator, puom.Numerator, puom.Unit, pr.UnitOfMeasure FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON pv.product_system_id = puom.ProductSystemId INNER JOIN PRODUCTS pr ON pv.product_id = pr.PRODUCT_ID WHERE pv.is_active = '{0}' AND ((puom.Unit = '{2}' or puom.Unit = '{3}') OR pr.UnitOfMeasure='{4}') AND pv.product_id = '{1}'".format(True, str(item.ProductId), uomMapping.CPQDisplayUOM,uomMapping.S4CPI,uom))
            #             #target_uomdata = ''
            #         else:
            #             uomdata = SqlHelper.GetFirst("SELECT pv.is_active, pv.product_id, puom.Denominator, puom.Numerator, puom.Unit, pr.UnitOfMeasure FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON pv.product_system_id = puom.ProductSystemId INNER JOIN PRODUCTS pr ON pv.product_id = pr.PRODUCT_ID WHERE pv.is_active = '{0}' AND (puom.Unit = '{2}' OR pr.UnitOfMeasure='{3}') AND pv.product_id = '{1}'".format(True,str(item.ProductId),uom,uom))
            #             #target_uomdata = SqlHelper.GetFirst("SELECT pv.is_active, pv.product_id, puom.Denominator, puom.Numerator, puom.Unit, pr.UnitOfMeasure FROM product_versions pv INNER JOIN sys_ProductSalesUnitOfMeasure puom ON pv.product_system_id = puom.ProductSystemId INNER JOIN PRODUCTS pr ON pv.product_id = pr.PRODUCT_ID WHERE pv.is_active = '{0}' AND (puom.Unit = '{2}' AND pr.UnitOfMeasure='{3}') AND pv.product_id = '{1}'".format(True,str(item.ProductId),'LBR',uom))
            #             #break
            #         #Trace.Write(uomdata.UnitOfMeasure)
            #         #TargetUOM_Change(item,uom) # updating the target UOM based on Unit Of Meassure change
            #         if uomdata:
            #             if uom != str(uomdata.UnitOfMeasure):
            #                 Trace.Write('11111')
            #                 item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT) * (float(uomdata.Numerator) / float(uomdata.Denominator))
            #                 item['LBF_QU_ExtCost'] = float(item['LBF_QU_MAT_CST']) * float(item.Quantity)
            #                 item['LBF_QU_NetWeight'] = round(float(result.NET_WEIGHT) * (float(uomdata.Numerator) / float(uomdata.Denominator)) * float(item.Quantity))
            #                 item['LBF_QU_WeightUnit'] = str(result.WEIGHT_UNIT)
            #             else:
            #                 Trace.Write('222222')
            #                 item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT)
            #                 item['LBF_QU_ExtCost'] = float(item['LBF_QU_MAT_CST']) * float(item.Quantity)
            #                 item['LBF_QU_NetWeight'] = float(result.NET_WEIGHT) * float(item.Quantity)
            #                 item['LBF_QU_WeightUnit'] = str(result.WEIGHT_UNIT)
            #         else:
            #             item['LBF_QU_MAT_CST'] = float(result.SAP_COST)/float(result.PRICE_UNIT)
            #             item['LBF_QU_WeightUnit'] = str(result.WEIGHT_UNIT)
            #             item['LBF_QU_NetWeight'] = float(result.NET_WEIGHT) * float(item.Quantity)
            #             item['LBF_QU_ExtCost'] = float(item['LBF_QU_MAT_CST']) * float(item.Quantity)


UOMCheck()