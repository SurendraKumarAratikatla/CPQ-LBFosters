def totalCost():
    try:
        for item in context.Quote.GetAllItems():
            Log.Info('LBF_QC_SP_TotalCost_Rail---->1111')
            if str(context.Quote.MarketId) != '13' and str(context.Quote.MarketId) != '8' and str(context.Quote.MarketId) != '12' and item.ProductName != 'CWR' and item.ProductName != 'CWR_QI':
                #if item.PartNumber[0] != 'R' and item.PartNumber[0] != 'B' and item.PartNumber[0] != '7':
                partNumber = str(item.PartNumber) if item.PartNumber else ''
                vcpPro = SqlHelper.GetList("SELECT * FROM PRODUCTS WHERE PRODUCT_CATALOG_CODE ='{0}' AND IsSyncedFromBackOffice ='True' AND IsSimple='False'".format(partNumber))

                matCost = item['LBF_QU_MAT_CST_OVR'] or item['LBF_QU_MAT_CST'] or 0
                freightCostExt = item['LBF_QU_FREIGHT_CST_EXT'] or 0
                handlingCostExt = item['LBF_QU_HANDLING_CST_EXT'] or 0
                freightCost = item['LBF_QU_FREIGHT_CST'] or 0
                handlingCost = item['LBF_QU_HANDLING_CST'] or 0
                quantity = float(item.Quantity or 1)

                item['LBF_QU_TOTAL_COST'] = str(float(matCost) + float(freightCostExt) + float(handlingCostExt))
                item['LBF_QU_COST_UN'] = str(float(matCost) + float(freightCost) + float(handlingCost))

                if item.ProductName not in ['Service for FM', 'FM Helper']:
                    if len(vcpPro) == 0:
                        item['LBF_QU_ExtCost'] = str(float(matCost) * quantity)
                    else:
                        item['LBF_QU_ExtCost'] = str(float(matCost))

                item['LBF_QU_TOTAL_COST'] = str(float(item['LBF_QU_ExtCost']) + float(freightCostExt) + float(handlingCostExt))

                gp_per = item['LBF_QU_GP_PER']
                if gp_per and float(gp_per) != 0:
                    total_cost = float(item['LBF_QU_TOTAL_COST']) / quantity
                    item['LBF_QU_SELPRICE_UN'] = str(total_cost / (1 - (float(gp_per)/100)))
                    Log.Info(str(item['LBF_QU_SELPRICE_UN']))
                    Log.Info('LBF_QC_SP_TotalCost_Rail 22222---->' + str(item['LBF_QU_SELPRICE_UN']))
                    item['LBF_QU_SELPRICE'] = str(round(float(item["LBF_QU_SELPRICE_UN"]), 2) * quantity)
                    #gross_profit_value = float(item['LBF_QU_SELPRICE']) - float(item['LBF_QU_TOTAL_COST']) if gp_per != 0 else 0.0
                    gross_profit_value = ((float(item['LBF_QU_SELPRICE_UN']) - float(total_cost))* quantity) if gp_per != 0 else 0.0
                    item['LBF_QU_GP_VAL'] = str(round(gross_profit_value, 2))
        
        #elif item.ProductName == 'CWR' or item.ProductName == 'CWR_QI':
            #item['LBF_QU_ExtCost'] = str(float(item['LBF_QU_MAT_CST']) * item.Quantity)
            #item['LBF_QU_SELPRICE'] = str(float(item['LBF_QU_SELPRICE_UN']) * item.Quantity)
            #item['LBF_QU_TOTAL_COST'] = str(float(item['LBF_QU_ExtCost']) + float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT']))
            #Log.Info('LBF_QC_SP_TotalCost_Rail-->'+str(float(item['LBF_QU_ExtCost']) + float(item['LBF_QU_FREIGHT_CST_EXT']) + float(item['LBF_QU_HANDLING_CST_EXT'])))
                
    except Exception as e:
        Log.Info("LBF_QC_SP_TotalCost_Rail error: "+str(e))
totalCost()
