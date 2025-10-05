class InforMat():
    def __init__(self):
        self.quoteInfo = context.Quote
        self.salesOrg = self.quoteInfo.SelectedMarket.Code
        

    def PriceCostUpdate(self):
        # for item in context.AffectedItems:
        for item in context.Quote.GetAllItems():
            proSystemId = item.ProductSystemId
            inforData = SqlHelper.GetFirst("select PART_SITE_ID,UNIT_COST_USD,UNIT_PRICE_USD from LBF_QU_INFOR_MAT_COST where PART_SITE_ID = '{0}'".format(proSystemId))
            if inforData:
                item['LBF_QU_COST_UN'] = inforData.UNIT_COST_USD
                item['LBF_QU_SELPRICE_UN'] = inforData.UNIT_PRICE_USD

    def run(self):
        self.PriceCostUpdate()


object = InforMat().run()