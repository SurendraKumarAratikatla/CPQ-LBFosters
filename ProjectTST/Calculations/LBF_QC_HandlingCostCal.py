class handling():
    def __init__(self):
        self.quoteInfo = context.Quote
        self.salesOrg = self.quoteInfo.SelectedMarket.Code
        

    def handlingCost(self):
        for item in context.AffectedItems:
            if item['LBF_QU_PLANT'] and self.salesOrg and item['LBF_QU_HANDLING_OB']:
                sqlHandlingData = SqlHelper.GetFirst("select SALESORG,PLANT,COST,VARIABLE from LBF_QU_HANDLING_COST where SALESORG = '{0}' and PLANT = '{1}' and VARIABLE = '{2}' ".format(self.salesOrg,item['LBF_QU_PLANT'],item['LBF_QU_HANDLING_OB']))
                if sqlHandlingData:
                    handlingCost = sqlHandlingData.COST
                    item['LBF_QU_HANDLING_CST'] = str(handlingCost)
                    if handlingCost and item.Quantity:
                        item['LBF_QU_HANDLING_CST_EXT'] = str(item['LBF_QU_HANDLING_CST'] * int(item.Quantity))
                    else:
                        item['LBF_QU_HANDLING_CST_EXT'] = "0.00"
                else:
                    item['LBF_QU_HANDLING_CST_EXT'] = "0.00"
            else:
                item['LBF_QU_HANDLING_CST_EXT'] = "0.00"

    def run(self):
        self.handlingCost()


object = handling().run()