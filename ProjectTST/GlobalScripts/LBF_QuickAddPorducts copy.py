class quickadd():
    def __init__(self, params):
        self.params = params

    def run(self):
        #Log.Info("LBF_QuickAddPorducts ---"+str(self.params))
        quickaddpro = SqlHelper.GetList("select TOP 5 * from PRODUCTS WHERE PRODUCT_NAME LIKE '{}'".format(str(self.params.searchval)+"%"))
        serData = JsonHelper.Serialize(quickaddpro).replace("PRODUCT_ID","id").replace("PRODUCT_NAME","name").replace("PRODUCT_CATALOG_CODE","partNumber").replace("PRODUCT_DESCRIPTION","description")
        data = JsonHelper.Deserialize(serData)
        # add missing fields
        for item in data:
            item['imageUrl'] = ""
            item['canAddToQuote'] = True
            item['addBtnDisabpledExplanation'] = ""
            item['isDiscontinued'] = False
            item['isConfigurableExternal'] = False
            item['isReplaced'] = False
            item['quantity '] = 1
            item['canAlterQuantity '] = True
            item['addToQuote'] = True
        #Log.Info("LBF_QuickAddPorducts data-------->"+str(data))
        return data


object = quickadd(Param).run()

ApiResponse = ApiResponseFactory.JsonResponse(object)