def totalCost():
    #try:
    for item in context.AffectedItems:
        Log.Info('LBF_QC_SP_TotalCost_Rail---->1111')
        if str(context.Quote.MarketId) != '13' and str(context.Quote.MarketId) != '8' and str(context.Quote.MarketId) != '12' and item.ProductName != 'CWR' and item.ProductName != 'CWR_QI':
            #if item.PartNumber[0] != 'R' and item.PartNumber[0] != 'B' and item.PartNumber[0] != '7':
            partNumber = str(item.PartNumber)
            vcpPro = SqlHelper.GetList("Select * from PRODUCTS where PRODUCT_CATALOG_CODE ='{0}' and IsSyncedFromBackOffice ='{1}' and IsSimple='{2}'".format(partNumber,'True','False'))

            matCost = item['LBF_QU_MAT_CST_OVR'] if item['LBF_QU_MAT_CST_OVR'] else item['LBF_QU_MAT_CST']
            item['LBF_QU_TOTAL_COST'] = str(float(matCost) + float(item['LBF_QU_FREIGHT_CST_EXT'] if item['LBF_QU_FREIGHT_CST_EXT'] else 0) + float(item['LBF_QU_HANDLING_CST_EXT'] if item['LBF_QU_HANDLING_CST_EXT'] else 0))
            item['LBF_QU_COST_UN'] = str(float(matCost) + float(item['LBF_QU_FREIGHT_CST']) + float(item['LBF_QU_HANDLING_CST']))
            if item.ProductName != 'Service for FM' or item.ProductName != 'FM Helper':
                if len(vcpPro) == 0:
                    item['LBF_QU_ExtCost'] = str((float(matCost)) * float(item.Quantity))
                else:
                    item['LBF_QU_ExtCost'] = str(float(matCost))
            item['LBF_QU_TOTAL_COST'] = str(float(item['LBF_QU_ExtCost']) + float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT']))
            #item['LBF_QU_SELPRICE_UN'] = item['LBF_QU_TOTAL_COST'] * item.Quantity
            if int(float(item['LBF_QU_GP_PER'])) != 0:
                total_cost = float(float(item['LBF_QU_TOTAL_COST'])) / float(item.Quantity)
                item['LBF_QU_SELPRICE_UN'] = str(float(total_cost) / (1-(float(item['LBF_QU_GP_PER'])/100)))
                Log.Info(str(item['LBF_QU_SELPRICE_UN']))
                Log.Info('LBF_QC_SP_TotalCost_Rail 22222---->'+str(item['LBF_QU_SELPRICE_UN']))
                item['LBF_QU_SELPRICE'] = str(float(round(item["LBF_QU_SELPRICE_UN"],2)) * float(item.Quantity))
        
        #elif item.ProductName == 'CWR' or item.ProductName == 'CWR_QI':
            #item['LBF_QU_ExtCost'] = str(float(item['LBF_QU_MAT_CST']) * item.Quantity)
            #item['LBF_QU_SELPRICE'] = str(float(item['LBF_QU_SELPRICE_UN']) * item.Quantity)
            #item['LBF_QU_TOTAL_COST'] = str(float(item['LBF_QU_ExtCost']) + float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT']))
            #Log.Info('LBF_QC_SP_TotalCost_Rail-->'+str(float(item['LBF_QU_ExtCost']) + float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT'])))
                
    #except Exception as e:
        # Log.Info("LBF_QC_SP_TotalCost_Rail error: "+str(e))
    #    pass
totalCost()
