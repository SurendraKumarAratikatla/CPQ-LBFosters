def totalCost():
    for item in context.AffectedItems:
        matCost = item['LBF_QU_MAT_CST_OVR'] if item['LBF_QU_MAT_CST_OVR'] else item['LBF_QU_MAT_CST']
        #item['LBF_QU_TOTAL_COST'] = str(float(matCost) + float(item['LBF_QU_FREIGHT_CST_EXT'] if item['LBF_QU_FREIGHT_CST_EXT'] else 0) + float(item['LBF_QU_HANDLING_CST_EXT'] if item['LBF_QU_HANDLING_CST_EXT'] else 0))
        item['LBF_QU_COST_UN'] = str(float(matCost) + item['LBF_QU_FREIGHT_CST'] + item['LBF_QU_HANDLING_CST'])
        item['LBF_QU_TOTAL_COST'] = str(float(item['LBF_QU_COST_UN']) * int(item.Quantity))
        Trace.Write(str(float(item['LBF_QU_COST_UN']) / (1-int(item['LBF_QU_GP_PER'])/100)))
        Trace.Write(str(float(item['LBF_QU_SELPRICE_UN']) * int(item.Quantity)))
        item['LBF_QU_SELPRICE_UN'] = str(float(item['LBF_QU_COST_UN']) / (1-int(item['LBF_QU_GP_PER'])/100))
        item['LBF_QU_SELPRICE'] = str(float(item['LBF_QU_SELPRICE_UN']) * int(item.Quantity))
        
totalCost()




#Cost/UoM = Mat.Cost.Override /Mat.Cost + Frt.Cost.Unit+Hnd.Cost.Unit
#Sell Price/UoM = Cost/UoM /(1-(Markup %/100))
#Total Sell Price = Sell Price/UoM * Quantity
