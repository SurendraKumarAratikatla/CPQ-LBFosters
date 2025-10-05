class addItems():
    def __init__(self):
        pass

    def whenAddItemsToCartTbl(self):
        for item in context.AffectedItems:
            # Log.Info("partnumber is---->"+str(item.PartNumber))
            partNumber = str(item.PartNumber)
            if partNumber:
                sqlLineData = SqlHelper.GetFirst("select * from LBF_QU_MAT_COST where MATERIAL = '{0}'".format(partNumber))
                if sqlLineData:
                    item['LBF_QU_MAT_CST'] = str(sqlLineData.SAP_COST)

        
    def run(self):
        self.whenAddItemsToCartTbl()


object = addItems().run()
