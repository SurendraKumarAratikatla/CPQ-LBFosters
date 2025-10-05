def currentItemVal():
    for item in context.AffectedItems:
        context.Quote.GetCustomField('LBF_CF_CurrentItemPlant').Value = item['LBF_QU_PLANT']
        context.Quote.GetCustomField('LBF_CF_CurrentItemHandling').Value = item['LBF_QU_HANDLING_OB']
        break
    
currentItemVal()