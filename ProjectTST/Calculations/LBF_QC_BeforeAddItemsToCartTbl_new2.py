for item in context.Quote.GetAllItems():
    uom = item.AsMainItem.UnitOfMeasure
    taruom = item["LBF_QU_TARUOM"]  # Safely get the value
    try:
        new_uom = SqlHelper.GetFirst("select * from LBF_QU_UOM_MAPPING_FIELDS where S4CPI='{0}'".format(uom)).CPQDisplayUOM
    except:
        new_uom = uom

    if "100#K" in item.Description and uom == "DR":
        item["LBF_QU_TARUOM"] = "KG1"
    elif "200#K" in item.Description and uom == "DR":
        item["LBF_QU_TARUOM"] = "KG2"
    elif "500#K" in item.Description and uom == "DR":
        item["LBF_QU_TARUOM"] = "KG5"
    else:
        if taruom:
            pass
        else:
            item["LBF_QU_TARUOM"] = new_uom

        if item["LBF_QU_TARUOM"]:
            if new_uom == "LB" and taruom.upper() not in ["TON", "KG"]:
                item["LBF_QU_TARUOM"] = "LB"

            elif new_uom != "LB":
                item["LBF_QU_TARUOM"] = new_uom

        # if taruom:  # Covers None, empty string, etc.
        #     item["LBF_QU_TARUOM"] = new_uom
        #     if uom == "LB":
        #         item["LBF_QU_TARUOM"] = "LB"
        #     else:
        #         item["LBF_QU_TARUOM"] = new_uom
        # else:
        #     if uom == "LB" and taruom.upper() not in ["TON", "KG"]:
        #         item["LBF_QU_TARUOM"] = "LB"
        #     elif taruom.upper() not in ["TON", "KG"]:
        #         item["LBF_QU_TARUOM"] = new_uom

    '''Log.Info("uom...."+str(uom))
    Log.Info("taruom...."+str(item["LBF_QU_TARUOM"]))
    if (str(uom) == "LB" and str(item["LBF_QU_TARUOM"]) != "LB") or str(item["LBF_QU_TARUOM"]) != str(uom):
        Log.Info("LBF_QC_BeforeAddItemsToCartTbl In ifff....")
        ScriptExecutor.Execute('LBF_GS_VCP_REQ_FIELDS_CHANGE')'''

class addItems():
    def __init__(self):
        pass

    def whenAddItemsToCartTbl(self):
        for item in context.Quote.GetAllItems():
            Log.Info("LBF_QC_BeforeAddItemsToCartTbl partnumber is---->"+str(item.PartNumber))
            partNumber = str(item.PartNumber)
            plant = item['LBF_QU_PLANT1']
            Trace.Write(item.ProductName)
            if partNumber:
                if item.ProductName != "CWR_QI":
                    sqlLineData = SqlHelper.GetFirst("select * from LBF_QU_MAT_COST where MATERIAL Like '%{0}' and Plant Like '%{1}'".format(partNumber,plant))
                    #partNumber = context.Product.PartNumber
                    vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))

                    if sqlLineData and not vcpPro:
                        cal_ = (float(sqlLineData.SAP_COST)/float(str(sqlLineData.PRICE_UNIT).replace(',','')))
                        item['LBF_QU_MAT_CST'] = cal_
                        Log.Info(str(item['LBF_QU_MAT_CST']))
                        item['LBF_QU_ExtCost'] = item['LBF_QU_MAT_CST'] * item.Quantity
                        #item['LBF_QU_MAT_CST_OVR'] = str(sqlLineData.SAP_COST)
                        Log.Info("running simple")
                    if item['LBF_QU_MAT_CST_OVR']:
                        item['LBF_QU_ExtCost'] = str(item['LBF_QU_MAT_CST_OVR'])
                        Log.Info('running vc')
                    else:
                        item['LBF_QU_ExtCost'] = str(item['LBF_QU_MAT_CST'])

        
    def run(self): 
        self.whenAddItemsToCartTbl()


object = addItems().run()
