def totalCost():
    for item in context.AffectedItems:
        matCost = item['LBF_QU_MAT_CST_OVR'] if item['LBF_QU_MAT_CST_OVR'] else item['LBF_QU_MAT_CST']
        item['LBF_QU_TOTAL_COST'] = str(float(matCost) + float(item['LBF_QU_FREIGHT_CST_EXT'] if item['LBF_QU_FREIGHT_CST_EXT'] else 0) + float(item['LBF_QU_HANDLING_CST_EXT'] if item['LBF_QU_HANDLING_CST_EXT'] else 0))
        item['LBF_QU_GP_VAL'] = str(float(item['LBF_QU_TOTAL_COST'] if item['LBF_QU_TOTAL_COST'] else 0) * float(item['LBF_QU_GP_PER'] if item['LBF_QU_GP_PER'] else 0) / 100)
        item['LBF_QU_SELPRICE'] = str(float(item['LBF_QU_TOTAL_COST'] if item['LBF_QU_TOTAL_COST'] else 0) + float(item['LBF_QU_GP_VAL'] if item['LBF_QU_GP_VAL'] else 0))
        item['LBF_QU_SELPRICE_UN'] = str(float(item['LBF_QU_SELPRICE'] if item['LBF_QU_SELPRICE'] else 0) / int(item.Quantity))

totalCost()